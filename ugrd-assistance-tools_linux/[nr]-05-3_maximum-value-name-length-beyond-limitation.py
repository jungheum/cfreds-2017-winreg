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

tree = h.node_add_child(h.root(), "0x05_TYPE3_VALUE-NAME-MAX")
set_value(tree, "", 1, "Root Node - a value name has a limit of 16,383 characters\0".encode('utf-16le'))

nk_name = "Value_Y"
node_y = h.node_add_child(tree, nk_name)
vk_name = ""
for idx in range(0, 16378): vk_name += "Y"
vk_name += "-16384"
set_value(node_y, vk_name, 1, "Y Node - a value name length is 16,384 characters\0".encode('utf-16le'))

nk_name = "Value_Z"
node_z = h.node_add_child(node_y, nk_name)
vk_name = ""
for idx in range(0, 32760): vk_name += "Z"
vk_name += "-32766"
set_value(node_z, vk_name, 1, "Z Node - a value name length is 32,766 characters\0".encode('utf-16le'))

h.commit(sys.argv[1])
