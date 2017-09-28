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

tree = h.node_add_child(h.root(), "0x02_TYPE2_TREE")

node_1 = h.node_add_child(tree, "Node_1")
set_value(node_1, "", 3, b"\x01")

node_11 = h.node_add_child(node_1, "Node_1-1")
set_value(node_11, "", 3, b"\x01\x01")

node_111 = h.node_add_child(node_11, "Node_1-1-1")
set_value(node_111, "", 3, b"\x01\x01\x01")

node_12 = h.node_add_child(node_1, "Node_1-2")
set_value(node_12, "", 3, b"\x01\x02")

node_121 = h.node_add_child(node_12, "Node_1-2-1")
set_value(node_121, "", 3, b"\x01\x02\x01")

node_2 = h.node_add_child(tree, "Node_2")
set_value(node_2, "", 3, b"\x02")

node_21 = h.node_add_child(node_2, "Node_2-1")
set_value(node_21, "", 3, b"\x02\x01")

node_211 = h.node_add_child(node_21, "Node_2-1-1")
set_value(node_211, "", 3, b"\x02\x01\x01")

node_212 = h.node_add_child(node_21, "Node_2-1-2")
set_value(node_212, "", 3, b"\x02\x01\x02")

node_22 = h.node_add_child(node_2, "Node_2-2")
set_value(node_22, "", 3, b"\x02\x02")

node_221 = h.node_add_child(node_22, "Node_2-2-1")
set_value(node_221, "", 3, b"\x02\x02\x01")

node_2211 = h.node_add_child(node_221, "Node_2-2-1-1")

node_222 = h.node_add_child(node_22, "Node_2-2-2")
set_value(node_222, "", 3, b"\x02\x02\x02")

node_2221 = h.node_add_child(node_222, "Node_2-2-2-1")

h.commit(sys.argv[1])
