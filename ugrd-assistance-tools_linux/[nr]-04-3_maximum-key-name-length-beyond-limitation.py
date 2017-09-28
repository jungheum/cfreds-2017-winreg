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

tree = h.node_add_child(h.root(), "0x04_TYPE3_KEY-NAME-MAX")

nk_name = "Node_"
for idx in range(0, 248): nk_name += "7"
nk_name += "-257"
node_7 = h.node_add_child(tree, nk_name)
set_value(node_7, "", 1, "1st Node - a key name length is 257 characters\0".encode('utf-16le'))

nk_name = "Node_"
for idx in range(0, 503): nk_name += "8"
nk_name += "-512"
node_8 = h.node_add_child(tree, nk_name)
set_value(node_8, "", 1, "2nd Node - a key name length is 512 characters\0".encode('utf-16le'))

nk_name = "Node_"
for idx in range(0, 1014): nk_name += "9"
nk_name += "-1024"
node_9 = h.node_add_child(tree, nk_name)
set_value(node_9, "", 1, "3rd Node - a key name length is 1024 characters\0".encode('utf-16le'))

h.commit(sys.argv[1])
