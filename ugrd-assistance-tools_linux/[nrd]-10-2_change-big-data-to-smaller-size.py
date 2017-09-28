# -*- coding: utf-8 -*-
import sys
import os
import hivex

assert not (len(sys.argv) != 2)
h = hivex.Hivex (sys.argv[1], verbose = True, debug = True, write = True)
assert h

def set_value(nk, vk_name, vk_type, vk_data):
    global h
    h.node_set_value(nk, {
        "key":   vk_name,
        "t":     vk_type,
        "value": vk_data
    })

child = h.node_get_child(h.root(), "0x06_TYPE2_BIG-DATA")

vk_name = "BINARY 20440"
vk_data = b""
for idx in range(0, 11): vk_data += "\xEE"
set_value(child, vk_name, 3, vk_data)

h.commit(sys.argv[1])
