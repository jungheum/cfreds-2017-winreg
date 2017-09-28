# -*- coding: utf-8 -*-
import sys
import os
import hivex

assert not (len(sys.argv) != 2)
h = hivex.Hivex (sys.argv[1], verbose = True, debug = True, write = True)
assert h

child = h.node_get_child(h.root(), "0x02_TYPE2_TREE")
child = h.node_get_child(child, "Node_2")
child = h.node_get_child(child, "Node_2-2")
child = h.node_get_child(child, "Node_2-2-1")
child = h.node_get_child(child, "Node_2-2-1-1")
h.node_delete_child(child)

child = h.node_get_child(h.root(), "0x02_TYPE2_TREE")
child = h.node_get_child(child, "Node_2")
child = h.node_get_child(child, "Node_2-2")
child = h.node_get_child(child, "Node_2-2-2")
child = h.node_get_child(child, "Node_2-2-2-1")
h.node_delete_child(child)

child = h.node_get_child(h.root(), "0x04_TYPE2_KEY-NAME-MAX")
child = h.node_get_child(child, "Node_222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222-255")
child = h.node_get_child(child, "Node_@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@-255")
h.node_delete_child(child)

h.commit(sys.argv[1])
