# -*- coding: utf-8 -*-
"""
=============================================================================
    * Description
        Version converter for Windows Registry hive file
        (v1.3 -> v1.5)
    * Author
        Jungheum Park (jungheum.park@nist.gov)
    * Organization
        Software and Systems Division
        Information Technology Laboratory
        National Institue of Standards and Technology
        U.S. Department of Commerce
    * Project @ NIST
        CFTT   (Computer Forensic Tool Testing)			www.cftt.nist.gov
        CFReDS (Computer Forensic Reference Data Sets)	www.cfreds.nist.gov
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

def xor32_checksum(buffer):
    sum = 0
    for i in range(0, 508, 4):
        # sum ^= struct.unpack('<I', buffer[i:i+4])[0]
        sum ^= int.from_bytes(buffer[i:i+4], byteorder='little')
    return sum

def patch_header(f, header):
    print('Original version : %d.%d' % (header[20], header[24]))
    print('Original checksum: %s' % hex(xor32_checksum(header)))
    header[24] = 0x05
    sum = xor32_checksum(header)
    # header[508:512] = struct.pack("<I", sum)
    header[508:512] = sum.to_bytes(4, byteorder='little')
    f.seek(0, os.SEEK_SET)
    f.write(header)
    print('Patched  version : %d.%d' % (header[20], header[24]))
    print('Patched  checksum: %s' % hex(sum))

f = open(sys.argv[1], 'rb+')
f.seek(0, os.SEEK_END)
size = f.tell()
if size > 512:
    f.seek(0, os.SEEK_SET)
    header = f.read(512)
    patch_header(f, bytearray(header))
f.flush()
f.close()
