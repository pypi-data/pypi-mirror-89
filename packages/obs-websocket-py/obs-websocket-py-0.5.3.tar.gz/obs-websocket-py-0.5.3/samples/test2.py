#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

import logging
logging.basicConfig(level=logging.DEBUG)

sys.path.append('../')
from obswebsocket import obsws, requests  # noqa: E402

host = "localhost"
port = 4444
password = "1"

ws = obsws(host, port, password)
ws.connect()

req = ws.call(requests.ToggleMute("noise"))

ws.disconnect()
