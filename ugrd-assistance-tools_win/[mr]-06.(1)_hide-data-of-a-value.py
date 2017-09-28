# -*- coding: utf-8 -*-
"""
=============================================================================
    * Description
        MR (manipulated registry hives) category
            > Primary class 1
              : Data hiding
            > Secondary class 6.1
              : Hide data of a value
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

def mr_pc1_sc6_1(buffer, filesize):
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
    vk_cell = None
    found = False
    
    while (1):
        if len(stack) == 0: break
        nk_cell = hive.get_nk(hive.calc_hive_offset(stack.pop()))
        sl_cell = hive.get_sl(hive.calc_hive_offset(nk_cell['base'].subkey_list_cell_offset))
        if nk_cell['base'].number_of_values > 0:
            # goto the value-list cell offset
            offset = hive.calc_hive_offset(nk_cell['base'].value_list_cell_offset)
            vl_cell = hive.get_vl(offset)
            for offset in vl_cell['offsets']:
                vk_cell = hive.get_vk(hive.calc_hive_offset(offset))
                data_size = vk_cell['base'].data_size
                if data_size & 0x80000000 == 0x80000000:
                    data_size = data_size & 0x7FFFFFFF
                # [condition] select a value cell which has BINARY type data (<= 16,344)
                if (4 < data_size and data_size <= 16344) and \
                   vk_cell['base'].data_type == 0x00000003: # REG_BINARY
                    found = True
                    break
            if found is True:
                break
        stack.extend(list(reversed(sl_cell['offsets'])))
    
    if nk_cell is None or vk_cell is None or found is False:
        return []
   
    # build manipulated item list (m_list)
    m_list = []
    m_item = {}
    m_item['offset'] = vk_cell['self'] + 0x08 # 'data size' in the vk cell
    edited_value = 0x00000000 # set to zero
    m_item['data'] = edited_value.to_bytes(4, byteorder='little')
    m_item['info'] = "[original size] 0x%08X (@ 0x%08X) --> [manipulated size] 0x%08X (@ 0x%08X)" \
                     % (vk_cell['base'].data_size, m_item['offset'], edited_value, m_item['offset'])
    m_item['info']+= "\n[Target 'vk_cell']\n: {}\n".format(vk_cell)
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
manipulate(f, sys.argv[1], mr_pc1_sc6_1(buffer, len(buffer)))
f.flush()
f.close()
