# -*- coding: utf-8 -*-
"""
=============================================================================
    * Description
        CR type #1 - A hive bin with Root key
        (CR means corrupted registry hives)
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
import struct
from ctypes import *

assert len(sys.argv) == 2

SIGNATURE_HIVE = "regf"
SIGNATURE_HBIN = "hbin"
FRAGMENT_HIVE_BLOCK = 0x1000 # normally 1 cluster in Windows OS
FIRST_HBIN_OFFSET = FRAGMENT_HIVE_BLOCK

class HIVE_HEADER(LittleEndianStructure):
    _fields_ = [
        ("signature",                 c_char*4),    
        ("primary_sequence_number",   c_int),       
        ("secondary_sequence_number", c_int),
        ("timestamp",                 c_ubyte*8),
        ("major_version",             c_int),
        ("minor_version",             c_int),
        ("file_type",                 c_int),
        ("unknown1",                  c_int),
        ("root_cell_offset",          c_int),
        ("last_hbin_offset",          c_int),
        ("unknown2",                  c_int),
        ("hivename",                  c_wchar*32),    
        ("unknown3",                  c_char*396),
        ("checksum",                  c_int)
    ]
 
class HIVE_BIN_HEADER(LittleEndianStructure):
    _fields_ = [
        ("signature",                 c_char*4),    
        ("offset",                    c_int),       
        ("size",                      c_int),
        ("unknown1",                  c_int),        
        ("unknown2",                  c_int),        
        ("timestamp",                 c_ubyte*8),
        ("unknown3",                  c_int)       
    ]
 
def static_cast(buffer, structure):
    return cast(c_char_p(buffer), POINTER(structure)).contents 
   
def cr_type1(buffer, filesize):
    # get the offset of root cell (0x24 from the beginning of hive file)
    header = static_cast(buffer[:sizeof(HIVE_HEADER)], HIVE_HEADER)    
    
    # traverse all hbin header cells
    hbins = []
    offset = FIRST_HBIN_OFFSET
    while 1:
        hbin_header = static_cast(buffer[offset:offset+sizeof(HIVE_BIN_HEADER)], HIVE_BIN_HEADER)
        if hbin_header.signature.decode("utf-8") != SIGNATURE_HBIN:
            break
        hbins.append((offset, hbin_header.size))
        offset += hbin_header.size
    
    # build corrupted fragment list (c_list) with specific conditions
    c_list = []
    for hbin in hbins:
        if hbin[0] < FIRST_HBIN_OFFSET + header.root_cell_offset and \
           FIRST_HBIN_OFFSET + header.root_cell_offset < hbin[0] + hbin[1]:
           c_list.append(hbin)
           break
    return c_list
    
def overwrite(fi, filename, c_list):
    fl = open(filename + '.txt', 'w', encoding='utf-8')
    for c_item in c_list:
        fi.seek(c_item[0], os.SEEK_SET)
        data = (b'NIST+CFTT+CFReDS' * int(c_item[1]/16))
        fi.write(data)
        fl.write('offset %04d \t\t size %04d\n' % (c_item[0], c_item[1]))
    fl.close()
      
      
f = open(sys.argv[1], 'rb+')
buffer = f.read()
overwrite(f, sys.argv[1], cr_type1(buffer, len(buffer)))
f.flush()
f.close()
