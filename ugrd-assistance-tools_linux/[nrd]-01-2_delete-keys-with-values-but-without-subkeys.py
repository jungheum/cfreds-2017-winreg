# -*- coding: utf-8 -*-
import sys
import os
import hivex

assert not (len(sys.argv) != 2)
h = hivex.Hivex (sys.argv[1], verbose = True, debug = True, write = True)
assert h

child = h.node_get_child(h.root(), "0x01_TYPE2_DATA-TYPES")
h.node_delete_child(child)

child = h.node_get_child(h.root(), "0x06_TYPE2_BIG-DATA")
h.node_delete_child(child)

h.commit(sys.argv[1])
