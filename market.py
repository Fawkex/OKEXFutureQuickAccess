#!/usr/bin/python
# -*- coding: utf-8 -*-
# encoding: utf-8
# 
# Copyright 2018 FawkesPan
#
# OkEX Future Quick Access
# Market Depth Real-time Subscription

import time
import ssl
import sys
import code
import json
import hashlib
import hmac
import urllib
import threading

from utils import buildMySign

import websocket

import string

try:
    import readline
except ImportError:
    pass

pong = time.time()

class WSSubscription:

    def __init__(self,api_key,api_secret,symbol='btc',contract_type='this_week'):
        self.__api_key = api_key
        self.__api_secret = api_secret
        self.__symbol = symbol
        self.__contract_type = contract_type
        self.__Depth = {}
        self.__Position = {}

        thread = threading.Thread(target=self.sub, args=())
        thread.daemon = True
        thread.start()

    def GetDepth(self):
        return self.__Depth

    def subscribe(self,ws):

        def run(*args):
            ws.send("{'event':'addChannel','channel':'ok_sub_futureusd_%s_depth_%s_5'}" % (self.__symbol,self.__contract_type))

            while True:
                ws.send("{'event':'ping'}")
                time.sleep(30)

        threading.Thread(target=run).start()

    def sub(self):

        websocket.enableTrace(False)
        URL = "wss://real.okex.com:10440/websocket/okexapi"
        ws = websocket.WebSocketApp(URL,
                                    on_message=self.incoming,
                                    on_error=self.error_handling,
                                    on_close=self.closing)

        ws.on_open = self.subscribe

        while True:
            try:
                ws.run_forever()
            except:
                pass

        pass

    def incoming(self,ws,message):
        global pong
        if 'pong' in message:
            pong = time.time()
        if 'asks' in message and 'bids' in message:
            d = json.loads(message)
            self.__Depth = d[0]['data']
    

    def error_handling(self,ws,error):
        print(str(error))

    def closing(self,ws):
        print("WebSocket Closing...")