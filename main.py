#!/usr/bin/python
# -*- coding: utf-8 -*-
# encoding: utf-8
# 
# Copyright 2018 FawkesPan
#
# OkEX Future Quick Access

# Hotkeys
OPEN_LONG = 'f1'
OPEN_SHORT = 'f2'
COVER_LONG = 'alt+f1'
COVER_SHORT = 'alt+f2'
COVER_ALL = 'alt+`'
CANCEL_ALL_PENDING = 'esc'

# Retry when failed to cover position
COVER_MAX_RETRIES = 5

import keyboard
import string
import apiconfig
import json
import time
import threading
import math

from market import WSSubscription
from future import OKCoinFuture

config = {}
config = apiconfig.get_config()
initial = 0
balance = 0
rights = 0
longCoverable = 0
shortCoverable = 0
is_refreshing = False

okcoinFuture = OKCoinFuture('www.okex.com',config['apiKey'],config['secretKey'])
market = WSSubscription(symbol=config['symbol'],contract_type=config['contract_type'])

if config['symbol'] != 'btc':
    contract_size = 10
else:
    contract_size = 100

def openLong():
    print('Opening Long Position...')
    if config['position'] == 0:
        amount = math.floor(balance * config['l_leverage'] * config['positionSize'] * market.GetDepth()['asks'][4][0] / contract_size)
    else:
        amount = math.ceil(config['positionSize'] * market.GetDepth()['asks'][4][0] / contract_size)

    grossValue = amount * (contract_size / market.GetDepth()['asks'][4][0])

    matchPrice = 0
    
    if config['orderMethod'] == 0:
        price = 0
        matchPrice = 1
        print('Placing a MARKET order...\nOrder size: %.4f %s' % (grossValue,config['symbol'].upper()))
    else:
        price = market.GetDepth()['bids'][0][0]
        print('Placing a LIMIT order at %.3f...\nOrder size: %.4f %s' % (price,grossValue,config['symbol'].upper()))

    try:
        order = json.loads(okcoinFuture.future_trade(config['symbol'] + "_usd",config['contract_type'],price=price,amount=amount,tradeType=1,matchPrice=matchPrice,leverRate=config['l_leverage']))['order_id']
        print('OrderID %s\n' % order)
    except:
        print('Failed to place order.')
    
    time.sleep(2)
    try:
        refreshPosition()
    except:
        pass

def openShort():
    print('Opening Short Position...')
    if config['position'] == 0:
        amount = math.floor(balance * config['s_leverage'] * config['positionSize'] * market.GetDepth()['bids'][0][0] / contract_size)
    else:
        amount = math.ceil(config['positionSize'] * market.GetDepth()['bids'][0][0] / contract_size)

    grossValue = amount * (contract_size / market.GetDepth()['bids'][0][0])

    matchPrice = 0

    if config['orderMethod'] == 0:
        price = 0
        matchPrice = 1
        print('Placing a MARKET order...\nOrder size: %.4f %s' % (grossValue,config['symbol'].upper()))
    else:
        price = market.GetDepth()['asks'][4][0]
        print('Placing a LIMIT order at %.3f...\nOrder size: %.4f %s' % (price,grossValue,config['symbol'].upper()))

    try:
        order = json.loads(okcoinFuture.future_trade(config['symbol'] + "_usd",config['contract_type'],price=price,amount=amount,tradeType=2,matchPrice=matchPrice,leverRate=config['s_leverage']))['order_id']
        print('OrderID %s\n' % order)
    except:
        print('Failed to place order.')

    time.sleep(2)
    try:
        refreshPosition()
    except:
        pass
    
def coverLong(nocheck=False):
    global longCoverable

    print('Closing Long Position...')

    if longCoverable == 0:
        try:
            refreshPosition()
        except:
            pass
        if longCoverable == 0:
            print("There is no position to be closed.")
            return

        
    amount = longCoverable

    grossValue = amount * (contract_size / market.GetDepth()['asks'][4][0])

    matchPrice = 0

    if config['orderMethod'] == 0:
        price = 0
        matchPrice = 1
        print('Placing a MARKET order...\nOrder size: %.4f %s' % (grossValue,config['symbol'].upper()))
    else:
        price = market.GetDepth()['asks'][4][0]
        print('Placing a LIMIT order at %.3f...\nOrder size: %.4f %s' % (price,grossValue,config['symbol'].upper()))

    i = 0
    
    while(True):
        i += 1
        try:
            order = json.loads(okcoinFuture.future_trade(config['symbol'] + "_usd",config['contract_type'],price=price,amount=amount,tradeType=3,matchPrice=matchPrice,leverRate=config['l_leverage']))['order_id']
            print('OrderID %s\n' % order)

            if nocheck == False:
                time.sleep(2)
                refreshPosition()
            
            return

        except:
            if i > COVER_MAX_RETRIES:
                print("Failed to place order after %s retries." % COVER_MAX_RETRIES)
                return
            
            print('Failed to place order. Retries %d/%d' % (i,COVER_MAX_RETRIES))
            
    

def coverShort(nocheck=False):
    global shortCoverable

    print('Closing Short Position...')

    if shortCoverable == 0:
        try:
            refreshPosition()
        except:
            pass
        if shortCoverable == 0:
            print("There is no position to be closed.")
            return

    amount = shortCoverable

    grossValue = amount * (contract_size / market.GetDepth()['bids'][0][0])

    matchPrice = 0

    if config['orderMethod'] == 0:
        price = 0
        matchPrice = 1
        print('Placing a MARKET order...\nOrder size: %.4f %s' % (grossValue,config['symbol'].upper()))
    else:
        price = market.GetDepth()['bids'][0][0]
        print('Placing a LIMIT order at %.3f...\nOrder size: %.4f %s' % (price,grossValue,config['symbol'].upper()))

    i = 0
    
    #print(json.loads(okcoinFuture.future_trade(config['symbol'] + "_usd",config['contract_type'],price=price,amount=amount,tradeType=4,matchPrice=matchPrice,leverRate=config['s_leverage'])))
    while(True):
        i += 1
        try:
            order = json.loads(okcoinFuture.future_trade(config['symbol'] + "_usd",config['contract_type'],price=price,amount=amount,tradeType=4,matchPrice=matchPrice,leverRate=config['s_leverage']))['order_id']
            print('OrderID %s\n' % order)

            if nocheck == False:
                time.sleep(2)
                refreshPosition()
            
            return

        except:
            if i > COVER_MAX_RETRIES:
                print("Failed to place order after %s retries." % COVER_MAX_RETRIES)
                return

            print('Failed to place order. Retries %d/%d' % (i,COVER_MAX_RETRIES))
            

def coverAll():
    print('Closing Positions...')

    coverLong(nocheck=True)
    coverShort(nocheck=True)
    
    time.sleep(2)
    refreshPosition()

def cancelAll():
    print('Canceling Orders...')
    while(True):
        try:
            orders = json.loads(okcoinFuture.future_orderinfo(config['symbol'] + "_usd",config['contract_type'],orderId=-1,status=1,currentPage=0,pageLength=50))['orders']
            orderids = ''
            i = 0
            for item in orders:
                i += 1
                orderids = orderids + str(item['order_id']) + ','
                if i == 3:
                    print(okcoinFuture.future_cancel(config['symbol'] + "_usd",config['contract_type'],orderids[:-1]))
                    orderids = ''
                    i = 0

            if i != 0:
                print(okcoinFuture.future_cancel(config['symbol'] + "_usd",config['contract_type'],orderids[:-1]))

            del orderids
            
            return

        except:
            pass

def refreshPosition():
    global longCoverable
    global shortCoverable
    global is_refreshing
    symbol = config['symbol'] + "_usd"

    if is_refreshing:
        return
    else:
        is_refreshing = True

    while(True):
        try:
            position = json.loads(okcoinFuture.future_position_4fix(config['symbol'] + "_usd",config['contract_type'],1))
            if position['result']:
                if symbol in str(position):
                    for item in position['holding']:
                        if item['buy_available'] != 0:
                            longCoverable = item['buy_available']
                            if item['lever_rate'] != config['l_leverage']:
                                print("Current long position is using leverage rate %d. Local setting has benn overrided." % item['lever_rate'])
                                config['l_leverage'] = item['lever_rate']

                        if item['sell_available'] != 0:
                            shortCoverable = item['sell_available']
                            if item['lever_rate'] != config['s_leverage']:
                                print("Current short position is using leverage rate %d. Local setting has benn overrided." % item['lever_rate'])
                                config['s_leverage'] = item['lever_rate']

                    is_refreshing = False
                    return
                else:
                    longCoverable = 0
                    shortCoverable = 0
                    
                    is_refreshing = False
                    return

        except:
            pass

def refresh():
    global balance
    global rights

    try:
        fix = json.loads(okcoinFuture.future_userinfo_4fix())['info'][config['symbol']]
        balance = fix['balance']
        rights = fix['rights']
    except:
        pass

def main():
    global longCoverable
    global shortCoverable
    global balance
    global rights
    global initial

    print('[Future Account Info]')
    fix = json.loads(okcoinFuture.future_userinfo_4fix())['info'][config['symbol']]
    balance = fix['balance']
    rights = fix['rights']
    initial = rights
    print(config['symbol'].upper() + " " + str(fix))
    print('[Maximum Order Size]\nLong %.4f\nShort %.4f\n' % (config['l_leverage'] * balance,config['s_leverage'] * balance))
    print('[Future Ticker]')
    print(config['symbol'].upper() + " " + str(okcoinFuture.future_ticker(config['symbol'] + "_usd",config['contract_type'])))
    print(config['contract_type'])
    print('\n[Hotkeys] \nOpen Long/' + OPEN_LONG.upper() + ' Open Short/' + OPEN_SHORT.upper() + '\nCover Long/' + COVER_LONG.upper() + ' Cover Short/' + COVER_SHORT.upper() + ' Cover All/' + COVER_ALL.upper() + '\nCancel All Orders/' + CANCEL_ALL_PENDING.upper() + '\n')

    #Binding Hotkeys
    keyboard.add_hotkey(OPEN_LONG, openLong, args=(), suppress=False, timeout=1, trigger_on_release=False)
    keyboard.add_hotkey(OPEN_SHORT, openShort, args=(), suppress=False, timeout=1, trigger_on_release=False)
    keyboard.add_hotkey(COVER_LONG, coverLong, args=(), suppress=False, timeout=1, trigger_on_release=False)
    keyboard.add_hotkey(COVER_SHORT, coverShort, args=(), suppress=False, timeout=1, trigger_on_release=False)
    keyboard.add_hotkey(COVER_ALL, coverAll, args=(), suppress=False, timeout=1, trigger_on_release=False)
    keyboard.add_hotkey(CANCEL_ALL_PENDING, cancelAll, args=(), suppress=False, timeout=1, trigger_on_release=False)

    def run(*args):
        i = 6
        while(True):
            i += 1
            refreshPosition()
            print()
            if i == 8:
                print(str(market.GetDepth()))
                print("\n[Account Info]\nCurrent Balance: %.4f \nCurrent Rights: %.4f \nProfit(Since this run): %.4f \n[Ticker Info]\nBuy: %.3f\nSell: %.3f" % (balance,rights,rights-initial,market.GetDepth()['bids'][0][0],market.GetDepth()['asks'][4][0]))
                print("[Position]\nLong Position: %d\nLeverage Rate: %d\nShort Position: %d\nLeverage Rate: %d\n" % (longCoverable,config['l_leverage'],shortCoverable,config['s_leverage']))
                i = 0

            time.sleep(2)

    time.sleep(2)
    threading.Thread(target=run).start()

if __name__ == '__main__':
    main()
