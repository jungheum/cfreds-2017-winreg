# -*- coding: utf-8 -*-
"""
=============================================================================
    * Description
        MR (manipulated registry hives) category
            > Primary class 1
              : Data hiding
            > Secondary class 1.1
              : Hide a Root key
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
       
def mr_pc1_sc1_1(buffer, filesize):
    # utilize the CFTT's hive class
    hive = cftt_hive(buffer)
    
    # get the offset of root cell (0x24 from the beginning of hive file)
    header = hive.get_header(0)
    offset = hive.calc_hive_offset(header.root_cell_offset)
    
    # goto the root cell
    root_cell = hive.get_nk(offset)
        
    # get the subkey-list cell of the root key cell
    offset = hive.calc_hive_offset(root_cell['base'].subkey_list_cell_offset)
    sl_cell = hive.get_sl(offset)
    
    if len(sl_cell['offsets']) == 0:
        return []
    
    # build manipulated item list (m_list)
    m_list = []
    m_item = {}
    m_item['offset'] = 0x24 # 'root key offset' in the hive header
    edited_value = sl_cell['offsets'][0]
    m_item['data'] = edited_value.to_bytes(4, byteorder='little')
    m_item['info'] = "[original offset] 0x%08X (@ 0x%08X) --> [manipulated offset] 0x%08X (@ 0x%08X)" \
                     % (header.root_cell_offset, m_item['offset'], edited_value, m_item['offset'])
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
manipulate(f, sys.argv[1], mr_pc1_sc1_1(buffer, len(buffer)))
f.flush()
f.close()
