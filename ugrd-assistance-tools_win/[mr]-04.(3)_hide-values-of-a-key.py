# -*- coding: utf-8 -*-
"""
=============================================================================
    * Description
        MR (manipulated registry hives) category
            > Primary class 1
              : Data hiding
            > Secondary class 4.3
              : Hide values of a key
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

BASE_COUNT = 7  # base value count
BASE_ADJUST = 4 # base adjust value
      
def mr_pc1_sc4_3(buffer, filesize):
    # utilize the CFTT's hive class
    hive = cftt_hive(buffer)
    
    # get the offset of root cell (0x24 from the beginning of hive file)
    header = hive.get_header(0)
    offset = hive.calc_hive_offset(header.root_cell_offset)
    
    # goto the root cell
    root_cell = hive.get_nk(offset)

    # get the 1st subkey offset of the original root key cell
    offset = hive.calc_hive_offset(root_cell['base'].subkey_list_cell_offset)
    sl_cell = hive.get_sl(offset)
        
    # traverse all subkeys
    stack = list(reversed(sl_cell['offsets']))
    nk_cell = None
    
    while (1):
        if len(stack) == 0: break
        nk_cell = hive.get_nk(hive.calc_hive_offset(stack.pop()))
        sl_cell = hive.get_sl(hive.calc_hive_offset(nk_cell['base'].subkey_list_cell_offset))
        # [condition] select a key cell which has at least BASE_COUNT values
        if nk_cell['base'].number_of_values >= BASE_COUNT:
            break            
        stack.extend(list(reversed(sl_cell['offsets'])))
    
    if nk_cell is None or \
       nk_cell['base'].number_of_values == 0:
        return []
    
    # goto the value-list cell offset
    offset = hive.calc_hive_offset(nk_cell['base'].value_list_cell_offset)
    vl_cell = hive.get_vl(offset)
    
    if nk_cell['base'].number_of_values != len(vl_cell['offsets']):
       print("Abnormal value is detected.")
    
    # build manipulated item list (m_list)
    m_list = []
    count = nk_cell['base'].number_of_values
    for i in range(count-BASE_ADJUST, count):
        m_item = {}
        # 'value offsets' in the value-list cell
        m_item['offset'] = vl_cell['self'] + 0x04 + i*4
        edited_value = 0x00000000 # set NULL bytes
        m_item['data'] = edited_value.to_bytes(4, byteorder='little')
        m_item['info'] = "[original offset] 0x%08X (@ 0x%08X) --> [manipulated offset] 0x%08X (@ 0x%08X)" \
                         % (vl_cell['offsets'][i], m_item['offset'], edited_value, m_item['offset'])
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
manipulate(f, sys.argv[1], mr_pc1_sc4_3(buffer, len(buffer)))
f.flush()
f.close()
