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
    
tree = h.node_add_child(h.root(), "0x07_TYPE2_NON-ASCII")
set_value(tree, "TEST 1", 1, u"Registry hive structure parsing\0".encode('utf-16le'))
set_value(tree, "TEST 2", 1, u"Non-ASCII characters\0".encode('utf-16le'))

items = [
    { "word"    : u"Hello", 
      "language": u"English\0" },
    { "word"    : u"¡Hola!", 
      "language": u"Spanish\0" },
    { "word"    : u"안녕하세요", 
      "language": u"Korean\0" },
    { "word"    : u"Здравствуйте", 
      "language": u"Russian\0" },
    { "word"    : u"您好", 
      "language": u"Chinese\0" },
    { "word"    : u"こんにちは", 
      "language": u"Japanese\0" },
    { "word"    : u"नमस्ते", 
      "language": u"Hindi\0" },
]

for item in items:
    name = item['word'].encode('utf-8')
    data = item['word'] + " : " + item['language']
    data = data.encode('utf-16le')
    node = h.node_add_child(tree, name)
    set_value(node, "", 1, item['language'].encode('utf-16le'))
    set_value(node, name, 1, data)   

h.commit(sys.argv[1])
