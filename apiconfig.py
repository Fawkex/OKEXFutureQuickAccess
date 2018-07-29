#!/usr/bin/python
# -*- coding: utf-8 -*-
# encoding: utf-8
# 
# Copyright 2018 FawkesPan
#
# OkEX Future Quick Access

# API链接信息
API_KEY = ''
SECRET_KEY = ''

# 开仓仓位大小
METHOD = 0                   # 0 按照百分比开仓 / 1 按照固定大小开仓
SIZE = 0.6                   # 按百分比开仓请填写小于1的数 按照固定大小开仓则填写开仓数量(以数字货币计 BTC合约最低为 100/BTC美元价格 其它币种合约为 10/币价)

# 开仓方法
ORDER_METHOD = 0             # 0 市价 / 1 按卖一价 买一价 限价挂单
LONG_LEVERAGE = 20           # 做多杠杆大小 10 或 20   #如程序运行时账号内已有仓位于此不符 则会按照账号内已有仓位的杠杆进行操作
SHORT_LEVERAGE = 20          # 做空杠杆大小 10 或 20   #如程序运行时账号内已有仓位于此不符 则会按照账号内已有仓位的杠杆进行操作

# 币种
CONTRACT = 'eos'             # btc/ltc/eth/etc/bch/eos/xrp
CONTRACT_TYPE = 'quarter'  # 当周 this_week 次周 next_week 季度 quarter

def get_config():
    config = {}

    config['apiKey'] = API_KEY
    config['secretKey'] = SECRET_KEY

    config['position'] = METHOD
    config['positionSize'] = SIZE

    config['orderMethod'] = ORDER_METHOD
    config['l_leverage'] = LONG_LEVERAGE
    config['s_leverage'] = SHORT_LEVERAGE

    config['symbol'] = CONTRACT
    config['contract_type'] = CONTRACT_TYPE

    return config