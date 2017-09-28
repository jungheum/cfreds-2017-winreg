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

tree = h.node_add_child(h.root(), "0x06_TYPE2_BIG-DATA")

vk_name = "BINARY 16344"
vk_data = b""
for idx in range(0, 16344): vk_data += "\x41"
set_value(tree, vk_name, 3, vk_data)

vk_name = "BINARY 16345"
vk_data = b""
for idx in range(0, 16345): vk_data += "\x42"
set_value(tree, vk_name, 3, vk_data)

vk_name = "BINARY 20440"
vk_data = b""
for idx in range(0, 20440): vk_data += "\x43"
set_value(tree, vk_name, 3, vk_data)

vk_name = "BINARY 32688"
vk_data = b""
for idx in range(0, 32688): vk_data += "\x44"
set_value(tree, vk_name, 3, vk_data)

# hivex-internal.h (line 329)
# define HIVEX_MAX_ALLOCATION  1000000
vk_name = "BINARY 1000000-4"
vk_data = b""
for idx in range(0, 1000000-4): vk_data += "\x45" 
set_value(tree, vk_name, 3, vk_data)

h.commit(sys.argv[1])
