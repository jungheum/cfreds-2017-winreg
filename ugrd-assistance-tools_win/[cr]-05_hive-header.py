# -*- coding: utf-8 -*-
"""
=============================================================================
    * Description
        CR type #5 - Hive header
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

assert len(sys.argv) == 2

FRAGMENT_HIVE_BLOCK = 0x1000 # normally 1 cluster in Windows OS

def cr_type5():
    c_list = [(0, FRAGMENT_HIVE_BLOCK)]
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
overwrite(f, sys.argv[1], cr_type5())
f.flush()
f.close()
