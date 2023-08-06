#!/usr/bin/env Python
# coding=utf-8
#作者： tony
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import websockets
import json,uuid,datetime
import asyncio
from Utils.Common import is_json, objtoLowerCase
from ws4py.client.threadedclient import WebSocketClient
from websocket import create_connection
import Utils.globalvar as glovar


# from SDK.RenderControl.IRenderControl import IRenderControl
# import threading
# import Utils.RenderViewer3D as CM
# async def opened(websocket):
#     # self.loop = asyncio.get_event_loop()
#     msg = json.dumps({"model":1,"Token":"d7b501d2-fe5d-4a26-a799-1e67e037bfb5"})
#     await websocket.send(msg)
#     return await websocket.recv()

# config={"serverAddress":"ws://124.193.151.47:8801/"}
# PropsTypeData = {}
# PropsValueData = {}
# PropsData = {}
# websocketcallback = None
# sdkInfoData = {}
# state = "F"
# apiCallback = {}
# websocket = None
# msg = {}
# eventCallback = {}

async def SocketApiServe_init(config):
    global _global_ws,_event_ws
    try:
        _global_ws= await websockets.connect(config.serverAddress)
        _event_ws=create_connection(config.serverAddress)
    except KeyboardInterrupt:
        await _global_ws.close(reason="user exit")



async def PostMessage(msg):
    # _global_ws=await glo.getWebSockets()
    await  _global_ws.send(msg)
    return await _global_ws.recv()


async def SendMessage(msg):
    # _global_ws=await glo.getWebSockets()
    await  _global_ws.send(msg)
    return True
#
# def getwebsocket():
#     global _global_ws
#     return _global_ws


async def recvmsg():
    # _global_ws=await glo.getWebSockets()
    await  _global_ws.recv()
    return True

def onMessage():
    msg=glovar.getcurloop().run_until_complete(recvmsg())
    return  msg
    # msg=ws.received_message()
    # msg=json.dumps({"model":1,"Token":"d7b501d2-fe5d-4a26-a799-1e67e037bfb5"})
    if is_json(msg):
        apiData = json.loads(msg)
        # apiData = apiData.get("Result")
        if "api" in apiData and "CallBack" in apiData:
            funName = apiData.get("api")
            if apiData.get("ErrorCode") is not None and apiData.get("ErrorCode")>0:
                raise Exception(apiData.get("Exception"))
            result = objtoLowerCase(apiData.get("Result"))
            if eventCallback["on" + funName]:
                sdkInfo(None, funName, "", "on")
                eventCallback["on" + funName](result)
            else:
                sdkInfo(None, apiData["CallBack"], "", "pull")
                apiCallback[apiData["CallBack"]](result)
                del apiCallback[apiData["CallBack"]]


    # msg=loopCur.run_until_complete(recv_msg())
    # msg=ws.received_message()
    # msg=json.dumps({"model":1,"Token":"d7b501d2-fe5d-4a26-a799-1e67e037bfb5"})

def postMessage(Props, callName, obj,isBack=True):
    # obj["CallBack"] = "API-{}".format(uuid.uuid1())
    # if Props is not None and callName is not None:
    #     sdkInfo(Props, obj.get("CallBack"), callName, "push")
    # loop = asyncio.get_event_loop()
    # str=loop.run_until_complete(send_msg(obj))
    if isBack:
        str=glovar.getcurloop().run_until_complete(PostMessage(json.dumps(obj)))
    else:
        str = glovar.getcurloop().run_until_complete(SendMessage(json.dumps(obj)))
    if is_json(str):
        apiData=json.loads(str)
        result = objtoLowerCase(apiData.get("Result"))
        # if apiData.get("CallBack") is not None:
        #     sdkInfo(None, apiData.get("CallBack"), "", "pull")
        #     apiCallback[apiData.get("CallBack")](result)
        #     del apiCallback[apiData.get("CallBack")]
        return result
    else:
        return str


def onMessageByEvent():
    print("this is event recv")
    aa=_event_ws.recv()
    print(aa)
    return aa

# def postMessage(msg):
#     loop = asyncio.get_event_loop()
#     loop.run_until_complete(send_msg(msg))

# def sdkInfo(Props, cbName, callName, type):
#     if cbName is None:
#         return
#     if type == "on":
#         pass
#     elif type == "pull":
#         if sdkInfoData[cbName] is not None:
#             className, _HashCode, time = sdkInfoData[cbName]
#             # console.info(className, _HashCode,"耗时",(performance.now() - time).toFixed(3) + "ms")
#             del sdkInfoData[cbName]
#     elif type == "push":
#         sdkInfoData[cbName] = {"time": datetime.datetime.now(),
#                                     "className": Props["propertyType"]["v"] + "." + callName,
#                                     "_HashCode": Props["_HashCode"]}
#     else:
#         pass
#
# def setCallBack(name,callback):
#     eventCallback[name]=callback

#
# def onMessage(that, resolve, type, data):
#         if type == "WEBSDK_API":  # 获取到websdk反馈的信息
#             if type(data) is str and "api" in data and "CallBack" in data:
#                 apiData = json.loads(data)
#                 name = apiData["api"]
#                 ErrorCode = apiData["ErrorCode"]
#                 Exception = apiData["Exception"]
#                 if ErrorCode > 0:
#                     raise Exception(Exception)
#                 result = objtoLowerCase(apiData["Result"])
#                 # if eventCallback["on" + name]:
#                 # sdkInfo(null, name, "", "on")
#                 # eventCallback["on" + name](result)
#                 # else:
#                 sdkInfo(None, apiData["CallBack"], "", "pull")
#                 apiCallback[apiData["CallBack"]](result)
#                 del apiCallback[apiData["CallBack"]]
#             else:
#                 raise Exception("ServerError:" + data)
#         elif type == "WEBSDK_START":  # 获取到 websdk服务可用
#             pass
#             # resolve(that)
#         elif type == "RENDER_FULL":  # 通过三维窗口实现的全屏功能
#             pass
#             # self.screenChange()
#         elif type == "WEBSDK_CONF":  # 由三维窗口提出的config数据获取
#             pass
#             # config = Object.assign({ clientState: self.clientState, isFull: self.isFull },self.config)
#             # print(config, self.params)
#             # renderWindow.postMessage({type: "WEBSDK_CONF",conf: JSON.stringify(config),params: JSON.stringify(self.params)},self.config.renderAddress)



# class givwebsocket(WebSocketClient):
#     def opened(self):
#         msg = json.dumps({"model": 1, "Token": "d7b501d2-fe5d-4a26-a799-1e67e037bfb5"})
#         self.send(msg)
#
#     def closed(self, code, reason=None):
#         print("Closed down", code, reason)
#
#     def received_message(self, m):
#         msg= str(m)
#         if len(msg)>0:
#             apiData = json.loads(msg)
#             # apiData = apiData.get("Result")
#             if "api" in apiData and "CallBack" in apiData:
#                 funName = apiData.get("api")
#                 if apiData.get("ErrorCode") is not None and apiData.get("ErrorCode") > 0:
#                     raise Exception(apiData.get("Exception"))
#                 result = objtoLowerCase(apiData.get("Result"))
#                 if eventCallback["on" + funName]:
#                     sdkInfo(None, funName, "", "on")
#                     eventCallback["on" + funName](result)
#                 else:
#                     sdkInfo(None, apiData["CallBack"], "", "pull")
#                     apiCallback[apiData["CallBack"]](result)
#                     del apiCallback[apiData["CallBack"]]

# ws= givwebsocket(CM["serverAddress"], protocols=['chat'])
# def start():
#     pass
#     try:
#         ws.connect()
#         ws.run_forever()
#     except KeyboardInterrupt:
#         ws.close()



