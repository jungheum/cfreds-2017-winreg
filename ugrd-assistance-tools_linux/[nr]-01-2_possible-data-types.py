# -*- coding: utf-8 -*-
import sys
import os
import hivex

assert not (len(sys.argv) != 2)
h = hivex.Hivex (sys.argv[1], verbose = True, debug = True, write = True)
assert h

child = h.node_add_child(h.root(), "0x01_TYPE2_DATA-TYPES")
assert child

#child = h.node_add_child(root, "0x01_DATA-TYPES")
#print h.node_name(child)
#print h.node_timestamp(child)
#assert child

values = [
    { "key"  : "VALUE 0x00 (NONE)", 
      "t"    : 0, 
      "value": b"\x6E\x6F\x6E\x65" },
    { "key"  : "VALUE 0x01 (SZ)", 
      "t"    : 1, 
      "value": u"UTF-16LE NULL-terminated string\0".encode('utf-16le') },
    { "key"  : "VALUE 0x02 (EXP_SZ)", 
      "t"    : 2, 
      "value": u"%SystemRoot%\0".encode('utf-16le') },
    { "key"  : "VALUE 0x03 (BINARY)", 
      "t"    : 3, 
      "value": b"\x62\x69\x6E\x61\x72\x79\x20\x64\x61\x74\x61" },		
    { "key"  : "VALUE 0x04 (DWORD-LE)", 
      "t"    : 4, 
      "value": b"\x04\x00\x00\x00" },			
    { "key"  : "VALUE 0x05 (DWORD-BE)", 
      "t"    : 5, 
      "value": b"\x00\x00\x00\x04" },	
    { "key"  : "VALUE 0x06 (LINK)", 
      "t"    : 6, 
      "value": u"Symbolic link\0".encode('utf-16le') },		
    { "key"  : "VALUE 0x07 (MULTI_SZ)", 
      "t"    : 7, 
      "value": u"REG_MULTI_SZ_1\0REG_MULTI_SZ_2\0REG_MULTI_SZ_3\0".encode('utf-16le') },				
    { "key"  : "VALUE 0x08 (RES_LIST)", 
      "t"    : 8, 
      "value": b"resource_list" },						
    { "key"  : "VALUE 0x09 (RES_DESC)", 
      "t"    : 9, 
      "value": b"resource_descriptor" },				
    { "key"  : "VALUE 0x0A (REQ_LIST)", 
      "t"    : 10, 
      "value": b"requirements_list" },		
    { "key"  : "VALUE 0x0B (QWORD-LE)", 
      "t"    : 11, 
      "value": b"\x08\x00\x00\x00\x00\x00\x00\x00" },				
]

h.node_set_values(child, values)
h.commit(sys.argv[1])
