#!/usr/bin/env Python
# coding=utf-8
#作者： tony

import os, sys,json,time
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import os, sys,types,json
import Utils.classmake as cmake
from websocket import create_connection
import threading
class EventThead(threading.Thread):
    def __init__(self, e, address):
        super().__init__()
        self.e = e
        self.address = address

    def run(self):
        ws1 = create_connection(self.address)
        while True:
            if self.e.is_set():
                # self.ws.recv()
                model = ws1.recv()
                backData=json.loads(model).get("api")
                if self.postData["EventName"]=="on"+backData:
                    cmake.AddRenderEventCB_ep(model, self.fn, self.fnName, self.eventArgs)
                self.e.wait()
                # self.e.clear()
            else:
                self.e.set()
                # print('runing')




def eventprocess_init(config):
    global eventprocess
    try:
        rcEvent = threading.Event()
        eventprocess = EventThead(rcEvent,config.serverAddress)
        # _global_ws.run_forever()
    except KeyboardInterrupt:
        pass

def EventProcessStart(fn,fnName,eventArgs,Props,callName,postData):
    eventprocess.fn = fn
    eventprocess.fnName = fnName
    eventprocess.eventArgs = eventArgs
    eventprocess.Props=Props
    eventprocess.callName=callName
    eventprocess.postData=postData
    eventprocess.start()



