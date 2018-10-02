#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests

FIAT_CURRENCY = 'USD'

from config.tokens import TOP_TOKENS, TOKENS

d = {}
for token in TOKENS:
    d[token['symbol']] = token

for token in TOP_TOKENS:
    result = requests.get('https://min-api.cryptocompare.com/data/price?fsym=%s&tsyms=%s' % (token, FIAT_CURRENCY)).json()
    if not FIAT_CURRENCY in result:
        print('%s (%s),0' % (token, d[token]['name']))
    else:
        print('%s (%s),%.2f' % (token, d[token]['name'], result[FIAT_CURRENCY]))
