#!/usr/bin/env python
# encoding:utf8;
"""
    * 作者：ChenJun
    * 时间：2020/12/28
    * 描述：
"""

import PyCRC
from PyCRC.crc import CRC

hex_str = "1234"
model = PyCRC.CRC_16_CCITT
crc = CRC.CRC(hex_str, model,True)
print(crc)

crc = CRC.CRC(hex_str, model)
print(crc)