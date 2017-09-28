# -*- coding: utf-8 -*-
"""
=============================================================================
    * Description
        MR (manipulated registry hives) category
            > Primary class 2
              : Infinite loop
            > Secondary class 1.1
              : Key loop
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

def mr_pc2_sc1_1(buffer, filesize):
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
        # [condition] select a key cell (except root) which has subkeys
        if (nk_cell['base'].number_of_subkeys > 0) and \
           (nk_cell['base'].flags & FLAG_NK_ROOT != FLAG_NK_ROOT):
            break
        stack.extend(list(reversed(sl_cell['offsets'])))
      
    if nk_cell is None or \
       nk_cell['base'].number_of_subkeys == 0 or \
       len(sl_cell['offsets']) == 0:
        return []
      
    # build manipulated item list (m_list)
    m_list = []
    m_item = {}
    
    # 'the last subkey offset' in the subkey-list cell
    count = nk_cell['base'].number_of_subkeys 
    m_item['offset'] = sl_cell['self'] + 0x08 + (count-1)*sl_cell['jump']
    edited_value = nk_cell['base'].parent_key_cell_offset # creating a loop
    m_item['data'] = edited_value.to_bytes(4, byteorder='little')
    m_item['info'] = "[original offset] 0x%08X (@ 0x%08X) --> [manipulated offset] 0x%08X (@ 0x%08X)" \
                     % (sl_cell['offsets'][count-1], m_item['offset'], edited_value, m_item['offset'])                      
    m_item['info']+= "\n[Target 'nk_cell']\n: {}\n".format(nk_cell)
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
manipulate(f, sys.argv[1], mr_pc2_sc1_1(buffer, len(buffer)))
f.flush()
f.close()
