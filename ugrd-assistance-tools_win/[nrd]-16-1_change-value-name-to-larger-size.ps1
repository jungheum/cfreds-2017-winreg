# NIST CFReDS - Change key name

Rename-ItemProperty -Path "HKLM:\ROOT\0x07_TYPE1_NON-ASCII" -Name "TEST 2" -NewName "TEEEEEEE 2"

Rename-ItemProperty -Path "HKLM:\ROOT\0x01_TYPE1_DATA-TYPES" -Name "VALUE 0x07 (MULTI_SZ)" -NewName "VEEEEEEE 0x07 (MULTI_SZ)"