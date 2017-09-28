# -*- coding: utf-8 -*-
"""
=============================================================================
    * Description
        MR (manipulated registry hives) category
            > Primary class 4
              : Version mismatch
            > Secondary class 1.1
              : Big data management (v1.3 -> v1.5)
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
from cftt_hive import *

assert len(sys.argv) == 2

def xor32_checksum(buffer):
    sum = 0
    for i in range(0, 508, 4):
        sum ^= int.from_bytes(buffer[i:i+4], byteorder='little')
    return sum

def mr_pc4_sc1_1(buffer, filesize):
    # utilize the CFTT's hive class
    hive = cftt_hive(buffer)
    
    # get the current version
    header_o = hive.get_header(0)
    header_m = hive.get_header(0)
    
    # change the minor version value
    if header_m.minor_version == 3:
        header_m.minor_version = 5
    elif header_m.minor_version == 5:
        header_m.minor_version = 3

    # update the checksum value
    header_m.checksum = xor32_checksum(bytearray(header_m))
    
    # build manipulated item list (m_list)
    m_list = []
    m_item = {}
    m_item['offset'] = 0 # start of the hive header
    m_item['data'] = bytearray(header_m)
    m_item['info'] = "[original version] %d.%d (@ 0x%08X) --> [manipulated version] %d.%d (@ 0x%08X)\n" \
                     % (header_o.major_version, header_o.minor_version, 0x14,
                        header_m.major_version, header_m.minor_version, 0x14)
    m_item['info'] += "[original checksum] 0x%08X (@ 0x%08X) --> [manipulated checksum] 0x%08X (@ 0x%08X)" \
                     % (header_o.checksum, 0x1FC,
                        header_m.checksum, 0x1FC)
    m_list.append(m_item)
    return m_list
    
def manipulate(fi, filename, m_list):
    fl = open(filename + '.txt', 'w', encoding='utf-8')
    if len(m_list) == 0:
        fl.write('There is no manipulated item.\n')    
    for m_item in m_list:
        fi.seek(m_item['offset'], os.SEEK_SET)
        fi.write(m_item['data'])
        fl.write(m_item['info'] + '\n')
    fl.close()
      
f = open(sys.argv[1], 'rb+')
buffer = f.read()
manipulate(f, sys.argv[1], mr_pc4_sc1_1(buffer, len(buffer)))
f.flush()
f.close()
