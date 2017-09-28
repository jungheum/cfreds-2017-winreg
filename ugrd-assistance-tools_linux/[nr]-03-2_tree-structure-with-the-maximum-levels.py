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

tree = h.node_add_child(h.root(), "0x03_TYPE2_TREE-MAX")
child = tree

for idx in range(3, 513):
    nk_name = '{:03d}'.format(idx)
    print nk_name
    child = h.node_add_child(child, nk_name)
	
set_value(child, "", 1, "A Registry tree can be 512 levels deep\0".encode('utf-16le'))

h.commit(sys.argv[1])
