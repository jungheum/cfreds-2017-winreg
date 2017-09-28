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

child = h.node_get_child(h.root(), "0x01_TYPE2_DATA-TYPES")

vk_name = "VALUE 0x01 (SZ)"
vk_data = u"UTF-EE NULL-terminated string\0".encode('utf-16le')
set_value(child, vk_name, 1, vk_data)

vk_name = "VALUE 0x03 (BINARY)"
vk_data = b"\x62\x69\xEE\xEE\x20\x64\x61\x74\x61"
set_value(child, vk_name, 3, vk_data)

h.commit(sys.argv[1])
