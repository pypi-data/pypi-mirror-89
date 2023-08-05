#!usr/bin/env python3
# -*- coding:utf-8 -*-
__author__ = 'yanqiong'

import asyncio
import json
import ssl
from abc import abstractmethod

import certifi
import websockets

from tqsdk.diff import _merge_diff, _get_obj
from tqsdk.entity import Entity
from tqsdk.utils import _generate_uuid

"""
优化代码结构，修改为

TqConnect 
（负责连接 websocket 连接，从服务器收到数据发回下游，从下游收到指令包发给上游，生成连接建立、连接断开的通知发给下游）
 ｜  ｜
TqReconnectHandler 
(连通上下游，记录重连发生时需要重新发送的数据，在发生重连时，暂停接受下游数据、暂停转发上游数据到下游，直到从上游收到的数据集是完整数据截面，继续恢复工作)
 ｜  ｜
 xxxxxx
 ｜  ｜
 api
"""


class TqConnect(object):
    """用于与 websockets 服务器通讯"""

    def __init__(self, logger) -> None:
        """
        创建 TqConnect 实例
        """
        self._logger = logger
        self._first_connect = True

    async def _run(self, api, url, send_chan, recv_chan):
        """启动websocket客户端"""
        self._api = api
        keywords = {
            "max_size": None,
            "extra_headers": self._api._base_headers
        }
        if url.startswith("wss://"):
            ssl_context = ssl.create_default_context()
            ssl_context.load_verify_locations(certifi.where())
            keywords["ssl"] = ssl_context
        while True:
            try:
                async with websockets.connect(url, **keywords) as client:
                    # 发送网络连接建立的通知，code = 2019112901
                    notify_id = _generate_uuid()
                    notify = {
                        "type": "MESSAGE",
                        "level": "INFO",
                        "code": 2019112901,
                        "content": "与 %s 的网络连接已建立" % url,
                        "url": url
                    }
                    if not self._first_connect:  # 如果不是第一次连接, 即为重连
                        # 发送网络连接重新建立的通知，code = 2019112902
                        notify["code"] = 2019112902
                        notify["level"] = "WARNING"
                        notify["content"] = "与 %s 的网络连接已恢复" % url
                        self._logger.debug("websocket reconnected")
                    else:
                        self._logger.debug("websocket connected")
                    # 发送网络连接建立的通知，code = 2019112901 or 2019112902，这里区分了第一次连接和重连
                    await recv_chan.send({
                        "aid": "rtn_data",
                        "data": [{
                            "notify": {
                                notify_id: notify
                            }
                        }]
                    })
                    send_task = self._api.create_task(self._send_handler(send_chan, client))
                    try:
                        async for msg in client:
                            self._logger.debug("websocket received data", pack=msg)
                            pack = json.loads(msg)
                            await recv_chan.send(pack)
                    finally:
                        send_task.cancel()
                        await send_task
            # 希望做到的效果是遇到网络问题可以断线重连, 但是可能抛出的例外太多了(TimeoutError,socket.gaierror等), 又没有文档或工具可以理出 try 代码中所有可能遇到的例外
            # 而这里的 except 又需要处理所有子函数及子函数的子函数等等可能抛出的例外, 因此这里只能遇到问题之后再补, 并且无法避免 false positive 和 false negative
            except (websockets.exceptions.ConnectionClosed, websockets.exceptions.InvalidStatusCode,
                    websockets.exceptions.InvalidState, websockets.exceptions.ProtocolError, OSError) as e:
                # 发送网络连接断开的通知，code = 2019112911
                notify_id = _generate_uuid()
                notify = {
                    "type": "MESSAGE",
                    "level": "WARNING",
                    "code": 2019112911,
                    "content": "与 %s 的网络连接断开，请检查客户端及网络是否正常" % url,
                    "url": url
                }
                self._logger.debug("websocket connection closed", error=str(e))
                await recv_chan.send({
                    "aid": "rtn_data",
                    "data": [{
                        "notify": {
                            notify_id: notify
                        }
                    }]
                })
            finally:
                if self._first_connect:
                    self._first_connect = False
            await asyncio.sleep(10)

    async def _send_handler(self, send_chan, client):
        """websocket客户端数据发送协程"""
        try:
            async for pack in send_chan:
                msg = json.dumps(pack)
                await client.send(msg)
                self._logger.debug("websocket send data", pack=msg)
        except asyncio.CancelledError:  # 取消任务不抛出异常，不然等待者无法区分是该任务抛出的取消异常还是有人直接取消等待者
            pass


class TqReconnect(object):
    def __init__(self, logger):
        self._logger = logger
        self._resend_request = {}  # 重连时需要重发的请求
        self._un_processed = False  # 重连后尚未处理完标志
        self._pending_diffs = []
        self._data = Entity()
        self._data._instance_entity([])

    async def _run(self, api, api_send_chan, api_recv_chan, ws_send_chan, ws_recv_chan):
        self._api = api
        send_task = self._api.create_task(self._send_handler(api_send_chan, ws_send_chan))
        try:
            async for pack in ws_recv_chan:
                self._record_upper_data(pack)
                if self._un_processed:  # 处理重连后数据
                    pack_data = pack.get("data", [])
                    self._pending_diffs.extend(pack_data)
                    for d in pack_data:
                        _merge_diff(self._data, d, self._api._prototype, False)
                    if self._is_all_received():
                        # 重连后收到完整数据截面
                        self._un_processed = False
                        pack = {
                            "aid": "rtn_data",
                            "data": self._pending_diffs
                        }
                        await api_recv_chan.send(pack)
                        self._logger = self._logger.bind(status=self._status)
                        self._logger.debug("data completed", pack=pack)
                    else:
                        await ws_send_chan.send({"aid": "peek_message"})
                        self._logger.debug("wait for data completed", pack={"aid": "peek_message"})
                else:
                    await api_recv_chan.send(pack)
                    is_reconnected = False
                    for d in pack.get("data", []):
                        for _, notify in d.get("notify", {}).items():
                            if notify["code"] == 2019112902:  # 重连建立
                                is_reconnected = True
                                break
                        if is_reconnected:
                            break
                    if is_reconnected:
                        self._un_processed = True
                        self._logger = self._logger.bind(status=self._status)
                        self._pending_diffs = []
                        self._data = Entity()
                        self._data._instance_entity([])
                        # 发送所有 resend_request
                        for msg in self._resend_request.values():
                            # 这里必须用 send_nowait 而不是 send，因为如果使用异步写法，在循环中，代码可能执行到 send_task, 可能会修改 _resend_request
                            ws_send_chan.send_nowait(msg)
                            self._logger.debug("resend request", pack=msg)
                        await ws_send_chan.send({"aid": "peek_message"})
        finally:
            send_task.cancel()
            await asyncio.gather(send_task, return_exceptions=True)

    async def _send_handler(self, api_send_chan, ws_send_chan):
        async for pack in api_send_chan:
            self._record_lower_data(pack)
            await ws_send_chan.send(pack)

    @property
    def _status(self):
        return "WAIT_FOR_COMPLETED" if self._un_processed else "READY"

    @abstractmethod
    def _is_all_received(self):
        """在重连后判断是否收到了全部的数据，可以继续处理后续的数据包"""
        pass

    def _record_upper_data(self, pack):
        """从上游收到的数据中，记录下重连时需要的数据"""
        pass

    def _record_lower_data(self, pack):
        """从下游收到的数据中，记录下重连时需要的数据"""
        pass


class MdReconnectHandler(TqReconnect):

    def _record_lower_data(self, pack):
        """从下游收到的数据中，记录下重连时需要的数据"""
        aid = pack.get("aid")
        if aid == "subscribe_quote":
            self._resend_request["subscribe_quote"] = pack
        elif aid == "set_chart":
            if pack["ins_list"]:
                self._resend_request[pack["chart_id"]] = pack
            else:
                self._resend_request.pop(pack["chart_id"], None)

    def _is_all_received(self):
        set_chart_packs = {k: v for k, v in self._resend_request.items() if v.get("aid") == "set_chart"}
        # 处理 seriesl(k线/tick)
        if not all([v.items() <= _get_obj(self._data, ["charts", k, "state"]).items()
                    for k, v in set_chart_packs.items()]):
            return False  # 如果当前请求还没收齐回应, 不应继续处理
        # 在接收并处理完成指令后, 此时发送给客户端的数据包中的 left_id或right_id 至少有一个不是-1 , 并且 mdhis_more_data是False；否则客户端需要继续等待数据完全发送
        if not all([(_get_obj(self._data, ["charts", k]).get("left_id", -1) != -1
                     or _get_obj(self._data, ["charts", k]).get("right_id", -1) != -1)
                    and not self._data.get("mdhis_more_data", True)
                    for k in set_chart_packs.keys()]):
            return False  # 如果当前所有数据未接收完全(定位信息还没收到, 或数据序列还没收到), 不应继续处理
        all_received = True  # 订阅K线数据完全接收标志
        for k, v in set_chart_packs.items():  # 判断已订阅的数据是否接收完全
            for symbol in v["ins_list"].split(","):
                if symbol:
                    path = ["klines", symbol, str(v["duration"])] if v["duration"] != 0 else ["ticks", symbol]
                    serial = _get_obj(self._data, path)
                    if serial.get("last_id", -1) == -1:
                        all_received = False
                        break
            if not all_received:
                break
        if not all_received:
            return False
        # 处理实时行情quote
        if self._data.get("ins_list", "") != self._resend_request.get("subscribe_quote", {}).get("ins_list", ""):
            return False  # 如果实时行情quote未接收完全, 不应继续处理
        return True


class TdReconnectHandler(TqReconnect):

    def __init__(self, logger):
        super().__init__(logger)
        self._pos_symbols = {}

    def _record_lower_data(self, pack):
        """从下游收到的数据中，记录下重连时需要的数据"""
        aid = pack.get("aid")
        if aid == "req_login":
            self._resend_request["req_login"] = pack
        elif aid == "confirm_settlement":
            self._resend_request["confirm_settlement"] = pack

    def _record_upper_data(self, pack):
        """从上游收到的数据中，记录下重连时需要的数据"""
        for d in pack.get("data", []):
            for user, trade_data in d.get("trade", {}).items():
                if user not in self._pos_symbols:
                    self._pos_symbols[user] = set()
                self._pos_symbols[user].update(trade_data.get("positions", {}).keys())

    def _is_all_received(self):
        """交易服务器只判断收到的 trade_more_data 是否为 False，作为收到完整数据截面的依据"""
        if not all([(not self._data.get("trade", {}).get(user, {}).get("trade_more_data", True))
                    for user in self._pos_symbols.keys()]):
            return False  # 如果交易数据未接收完全, 不应继续处理
        # 有可能重连之后，持仓比原有持仓减少，需要原有的数据集中删去减少的合约的持仓
        for user, trade_data in self._data.get("trade", {}).items():
            symbols = set(trade_data.get("positions", {}).keys())  # 当前真实持仓中的合约
            if self._pos_symbols.get(user, set()) > symbols:  # 如果此用户历史持仓中的合约比当前真实持仓中更多: 删除多余合约信息
                self._pending_diffs.append({
                    "trade": {
                        user: {
                            "positions": {symbol: None for symbol in (self._pos_symbols[user] - symbols)}
                        }
                    }
                })
        return True
