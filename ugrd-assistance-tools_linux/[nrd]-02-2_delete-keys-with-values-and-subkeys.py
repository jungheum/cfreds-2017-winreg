# -*- coding: utf-8 -*-
import sys
import os
import hivex

assert not (len(sys.argv) != 2)
h = hivex.Hivex (sys.argv[1], verbose = True, debug = True, write = True)
assert h

child = h.node_get_child(h.root(), "0x02_TYPE2_TREE")
child = h.node_get_child(child, "Node_1")
h.node_delete_child(child)

child = h.node_get_child(h.root(), "0x02_TYPE2_TREE")
child = h.node_get_child(child, "Node_2")
h.node_delete_child(child)

child = h.node_get_child(h.root(), "0x07_TYPE2_NON-ASCII")
h.node_delete_child(child)

h.commit(sys.argv[1])
