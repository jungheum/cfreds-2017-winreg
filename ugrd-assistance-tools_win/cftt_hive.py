# -*- coding: utf-8 -*-
"""
=============================================================================
    * Description
        common class for handling the hive format
    * Author
        Jungheum Park (jungheum.park@nist.gov)
    * Organization
        Software and Systems Division
        Information Technology Laboratory
        National Institue of Standards and Technology
        U.S. Department of Commerce
    * Project @ NIST
        CFTT   (Computer Forensic Tool Testing)         www.cftt.nist.gov
        CFReDS (Computer Forensic Reference Data Sets)  www.cfreds.nist.gov
    * License
        Apache License 2.0
    * Tested Environment
        Windows 7 Enterprise SP1 64-bits English
        Python 3.4.3
=============================================================================
"""
import sys
import os
from ctypes import *

SIGNATURE_HIVE = "regf"
SIGNATURE_HBIN = "hbin"
FRAGMENT_HIVE_BLOCK = 0x1000 # normally 1 cluster in Windows OS
FIRST_HBIN_OFFSET = FRAGMENT_HIVE_BLOCK
FLAG_NK_ROOT = 0x0004
FLAG_NK_ASCII = 0x0020
FLAG_VK_ASCII = 0x0001

class HIVE_HEADER(LittleEndianStructure):
    _fields_ = [
        ("signature",                 c_char*4),    
        ("primary_sequence_number",   c_uint),       
        ("secondary_sequence_number", c_uint),
        ("timestamp",                 c_ubyte*8),
        ("major_version",             c_uint),
        ("minor_version",             c_uint),
        ("file_type",                 c_uint),
        ("unknown1",                  c_uint),
        ("root_cell_offset",          c_uint),
        ("last_hbin_offset",          c_uint),
        ("unknown2",                  c_uint),
        ("hivename",                  c_wchar*32),    
        ("unknown3",                  c_char*396),
        ("checksum",                  c_uint)
    ]
 
class HIVE_BIN_HEADER(LittleEndianStructure):
    _fields_ = [
        ("signature",                 c_char*4),    
        ("offset",                    c_uint),       
        ("size",                      c_uint),
        ("unknown1",                  c_uint),        
        ("unknown2",                  c_uint),        
        ("timestamp",                 c_ubyte*8),
        ("unknown3",                  c_uint)       
    ]
 
class HIVE_CELL_NK(LittleEndianStructure):
    _fields_ = [
        ("cell_size",                 c_int),
        ("signature",                 c_char*2),
        ("flags",                     c_ushort),
        ("timestamp",                 c_ubyte*8),
        ("unknown1",                  c_uint),
        ("parent_key_cell_offset",    c_uint),
        ("number_of_subkeys",         c_uint),
        ("number_of_volatile_subkeys",c_uint),
        ("subkey_list_cell_offset",   c_uint),
        ("v_subkey_list_cell_offset", c_uint),
        ("number_of_values",          c_uint),
        ("value_list_cell_offset",    c_uint),
        ("security_cell_offset",      c_uint),
        ("class_name_offset",         c_uint),
        ("max_subkey_name_size",      c_uint),
        ("max_subkey_class_name_size",c_uint),
        ("max_value_name_size",       c_uint),
        ("max_data_size",             c_uint),
        ("unknown2",                  c_uint),
        ("key_name_size",             c_ushort),
        ("class_name_size",           c_ushort)
    ]

# HIVE_CELL_NK - FLAGS
# --------------------------
# 0x0001      volatile key
# 0x0002      mount point (of another Registry hive)
# 0x0004      root key
# 0x0008      cannot be deleted
# 0x0010      symbolic link key
# 0x0020      ASCII name (otherwise UTF-16LE name)
# 0x0040      predefined handle    
    
# subkey-list cell
class HIVE_CELL_SL(LittleEndianStructure):
    _fields_ = [
        ("cell_size",                 c_int),
        ("signature",                 c_char*2),
        ("number_of_subkeys",         c_ushort),
    ]

# value-list cell
class HIVE_CELL_VL(LittleEndianStructure):
    _fields_ = [
        ("cell_size",                 c_int)
    ]

class HIVE_CELL_VK(LittleEndianStructure):
    _fields_ = [
        ("cell_size",                 c_int),
        ("signature",                 c_char*2),
        ("value_name_size",           c_ushort),
        ("data_size",                 c_uint),
        ("data_cell_offset",          c_uint),
        ("data_type",                 c_uint),
        ("flags",                     c_ushort),
        ("unknown1",                  c_ushort),
    ]    

# HIVE_CELL_VK - DATA TYPES
# --------------------------
# 0x00000000  REG_NONE
# 0x00000001  REG_SZ
# 0x00000002  REG_EXPAND_SZ
# 0x00000003  REG_BINARY
# 0x00000004  REG_DWORD (= REG_DWORD_LITTLE_ENDIAN)
# 0x00000005  REG_DWORD_BIG_ENDIAN
# 0x00000006  REG_LINK
# 0x00000007  REG_MULTI_SZ
# 0x00000008  REG_RESOURCE_LIST
# 0x00000009  REG_FULL_RESOURCE_DESCRIPTOR
# 0x0000000a  REG_RESOURCE_REQUIREMENTS_LIST
# 0x0000000b  REG_QWORD (= REG_QWORD_LITTLE_ENDIAN)

# HIVE_CELL_VK - FLAGS
# --------------------------
# 0x0001      ASCII name

# data cell
class HIVE_CELL_DATA(LittleEndianStructure):
    _fields_ = [
        ("cell_size",                 c_int)
    ]

# big-data cell
class HIVE_CELL_BDATA(LittleEndianStructure):
    _fields_ = [
        ("cell_size",                 c_int),
        ("signature",                 c_char*2),
        ("number_of_segments",        c_short),
    ]
# data-block-segment-list cell
class HIVE_CELL_DL(LittleEndianStructure):
    _fields_ = [
        ("cell_size",                 c_int),
    ]
    
def static_cast(buffer, structure):
    return cast(c_char_p(buffer), POINTER(structure)).contents 
    
#---------------------------------------------------------------
# cftt hive class
#
class cftt_hive:

    def __init__(self, buffer):
        self.buffer = buffer # support simple memory operations only
                             # for CFReDS & CFTT works
                             # (it can be updated for file operations)
        return
   
    def calc_hive_offset(self, offset):
        return FRAGMENT_HIVE_BLOCK + offset
   
    def get_header(self, offset):
        header = static_cast(self.buffer[offset:offset+sizeof(HIVE_HEADER)], HIVE_HEADER)
        return header
   
    def get_nk(self, offset):
        nk_cell = {}
        nk_cell['self'] = offset
        nk_cell['base'] = static_cast(self.buffer[offset:offset+sizeof(HIVE_CELL_NK)], HIVE_CELL_NK)
        nk_cell['key_name'] = ''
        
        offset += sizeof(HIVE_CELL_NK)
        if nk_cell['base'].flags & FLAG_NK_ASCII == FLAG_NK_ASCII:
            # name is encoded by ASCII
            nk_cell['key_name'] = self.buffer[offset:offset+nk_cell['base'].key_name_size].decode('cp1252')
        else:
            # name is encoded by UTF-16LE
            nk_cell['key_name'] = self.buffer[offset:offset+nk_cell['base'].key_name_size].decode('utf-16le')
            
        return nk_cell
          
    def get_sl(self, offset): # subkey-list cell
        sl_cell = {}
        sl_cell['self'] = offset
        sl_cell['base'] = static_cast(self.buffer[offset:offset+sizeof(HIVE_CELL_SL)], HIVE_CELL_SL)
        sl_cell['offsets'] = []
        sl_cell['jump'] = 8
        
        offset += sizeof(HIVE_CELL_SL)
        if sl_cell['base'].signature.decode('utf-8') == 'ri' or \
           sl_cell['base'].signature.decode('utf-8') == 'li':
           sl_cell['jump'] = 4
        
        for i in range(sl_cell['base'].number_of_subkeys):
            temp = self.buffer[(offset+i*sl_cell['jump']):(offset+i*sl_cell['jump'])+4]
            #print(int.from_bytes(temp, byteorder='little'))
            sl_cell['offsets'].append(int.from_bytes(temp, byteorder='little'))    
            
        return sl_cell
 
    def get_vl(self, offset): # value-list cell
        vl_cell = {}
        vl_cell['self'] = offset
        vl_cell['base'] = static_cast(self.buffer[offset:offset+sizeof(HIVE_CELL_VL)], HIVE_CELL_VL)
        vl_cell['offsets'] = []
        
        if vl_cell['base'].cell_size > 0:
            return vl_cell
        
        offset += sizeof(HIVE_CELL_VL)
        for i in range(int((-vl_cell['base'].cell_size-4)/4)):
            temp = self.buffer[(offset+i*4):(offset+i*4)+4]
            temp = int.from_bytes(temp, byteorder='little')
            if temp == 0: continue
            vl_cell['offsets'].append(temp)
            
        return vl_cell
        
    def get_vk(self, offset):
        vk_cell = {}
        vk_cell['self'] = offset
        vk_cell['base'] = static_cast(self.buffer[offset:offset+sizeof(HIVE_CELL_VK)], HIVE_CELL_VK)
        vk_cell['value_name'] = ''
        
        offset += sizeof(HIVE_CELL_VK)
        if vk_cell['base'].flags & FLAG_VK_ASCII == FLAG_VK_ASCII:
            # name is encoded by ASCII
            vk_cell['value_name'] = self.buffer[offset:offset+vk_cell['base'].value_name_size].decode('cp1252')
        else:
            # name is encoded by UTF-16LE
            vk_cell['value_name'] = self.buffer[offset:offset+vk_cell['base'].value_name_size].decode('utf-16le')
            
        return vk_cell
          
    def get_data(self, offset): # data cell
        data_cell = {}
        data_cell['self'] = offset
        data_cell['base'] = static_cast(self.buffer[offset:offset+sizeof(HIVE_CELL_DATA)], HIVE_CELL_DATA)
        return data_cell
        
