# -*- coding: utf-8 -*-
"""
=============================================================================
    * Description
        MR (manipulated registry hives) category
            > Primary class 5
              : Ambiguous encoding
            > Secondary class 3.1
              : Different encodings
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
        Python 2.7.9
        =>| '_winreg' module in Python 2.7 is used for this sub-class
          | because 'winreg' module in Python 3.x supports 
          | writing UTF-16LE encoded strings only.
=============================================================================
"""
import _winreg

def mr_pc5_sc3_1():
    # get the root key
    root = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, "ROOT")
    
    # create the a key with a value
    parent = _winreg.CreateKey(root, "0x08_AMBIGUOUS-ENCODING")
    data = u"ISO-8859-15, EUC-KR, KOI8-R, GB18030, EUC-JP, UTF-8"
    _winreg.SetValueEx(parent, "Different encodings", 0, _winreg.REG_SZ, data)
    
    items = [
        { "encoding": "ISO8859-15",
          "word"    : u"¡Hola!", 
          "language": u"Spanish" },
        { "encoding": "EUC-KR",
          "word"    : u"안녕하세요", 
          "language": u"Korean" },
        { "encoding": "KOI8-R",
          "word"    : u"Здравствуйте", 
          "language": u"Russian" },
        { "encoding": "GB18030",
          "word"    : u"您好", 
          "language": u"Chinese" },
        { "encoding": "EUC-JP",
          "word"    : u"こんにちは", 
          "language": u"Japanese" },
        { "encoding": "UTF-8",
          "word"    : u"नमस्ते", 
          "language": u"Hindi" },
    ]
        
    for item in items:
        name = item['word'].encode(item['encoding'])
        data = item['word'] + " : " + item['language'] + " encoded by " + item['encoding']
        data = data.encode(item['encoding'])
        key = _winreg.CreateKey(parent, name)
        _winreg.SetValueEx(key, "", 0, _winreg.REG_SZ, item['language'])
        _winreg.SetValueEx(key, name, 0, _winreg.REG_SZ, data)
        _winreg.SetValueEx(key, "Encoding", 0, _winreg.REG_SZ, item['encoding'])
       
    return
    
mr_pc5_sc3_1()
