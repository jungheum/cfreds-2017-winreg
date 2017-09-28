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

tree = h.node_add_child(h.root(), "0x05_TYPE2_VALUE-NAME-MAX")
set_value(tree, "", 1, "Root Node - a value name has a limit of 16,383 characters\0".encode('utf-16le'))

nk_name = "Value_V"
node_v = h.node_add_child(tree, nk_name)
vk_name = ""
for idx in range(0, 16377): vk_name += "V"
vk_name += "-16383"
set_value(node_v, vk_name, 1, "V Node - a value name has a limit of 16,383 characters\0".encode('utf-16le'))

nk_name = "Value_W"
node_w = h.node_add_child(node_v, nk_name)
vk_name = ""
for idx in range(0, 16377): vk_name += "W"
vk_name += "-16383"
set_value(node_w, vk_name, 1, "W Node - a value name has a limit of 16,383 characters\0".encode('utf-16le'))

h.commit(sys.argv[1])
