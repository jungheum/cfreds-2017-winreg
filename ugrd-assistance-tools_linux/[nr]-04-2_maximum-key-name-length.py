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

tree = h.node_add_child(h.root(), "0x04_TYPE2_KEY-NAME-MAX")

nk_name = "Node_"
for idx in range(0, 246): nk_name += "1"
nk_name += "-255"
node_1 = h.node_add_child(tree, nk_name)
set_value(node_1, "", 1, "1st Node - a key name has a limit of 255 characters\0".encode('utf-16le'))

nk_name = "Node_"
for idx in range(0, 246): nk_name += "2"
nk_name += "-255"
node_2 = h.node_add_child(tree, nk_name)
set_value(node_2, "", 1, "2nd Node - a key name has a limit of 255 characters\0".encode('utf-16le'))

nk_name = "Node_"
for idx in range(0, 246): nk_name += "@"
nk_name += "-255"
h.node_add_child(node_2, nk_name)

nk_name = "Node_"
for idx in range(0, 246): nk_name += "$"
nk_name += "-255"
h.node_add_child(node_2, nk_name)

nk_name = "Node_"
for idx in range(0, 247): nk_name += "3"
nk_name += "-256"
node_3 = h.node_add_child(tree, nk_name)
set_value(node_3, "", 1, "3rd Node - the maximum length of a key name may be 256 characters if there is no NULL character\0".encode('utf-16le'))

h.commit(sys.argv[1])
