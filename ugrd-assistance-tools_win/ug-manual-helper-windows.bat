@echo off
setlocal enabledelayedexpansion
title NIST CFReDS - User-Generated Reference Registry Generator in Windows Environment
bcdedit /enum bootmgr > nul || goto :admin

::-----------------------------------------------------------------------------------------------
goto comment
	* Description
		Automation script for creating user-generated reference registry hives 
		in Windows environment (for manual operation)
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
		Windows  7 Enterprise SP1 64-bits English
        Windows 10 Home 64-bits English
		Python 2.7.9 (assume that the installation path is "c:\python27\python.exe")
		Python 3.4.3 (assume that the installation path is "c:\python34\python.exe")
:comment

echo.
echo  * User-Generated Reference Registry Hive File Generator in Windows Environment (for manual operation)
echo.
echo  * Developed and managed by
echo    ^- NIST CFTT   (Computer Forensic Tool Testing)         www.cftt.nist.gov
echo    ^- NIST CFReDS (Computer Forensic Reference Data Sets)  www.cfreds.nist.gov
echo.

::-----------------------------------------------------------------------------------------------
echo   ^-----------------------------------------------------------------------------------------
echo   == Set global variables
:set_global_variables
    set all_in_one_hive=[nr]-##-1_all-in-one
	REM set all_in_one_hive_v13=[nr]-##-1_all-in-one_v13.hive
    REM set all_in_one_hive_v15=[nr]-##-1_all-in-one_v15.hive
    
	:: get the current local date & time
	for /f "usebackq tokens=1,2 delims==" %%i in (`wmic os get LocalDateTime /VALUE 2^>nul`) do (
		if '.%%i.'=='.LocalDateTime.' set ldt=%%j
	)
	set timestamp=%ldt:~0,4%-%ldt:~4,2%-%ldt:~6,2% %ldt:~8,2%.%ldt:~10,2%.%ldt:~12,2%
	set base_outdir=%~dp0[%timestamp%] User-Generated Registry Hives using WinAPI (manual operation)\
	mkdir "%base_outdir%"

::-----------------------------------------------------------------------------------------------		
:job_manager
	:: generate reference hive files manually
	call :execute_manual_operations "v13" "[nrd]-11-2_change-key-name-and-remain-original-size"
    call :execute_manual_operations "v15" "[nrd]-11-2_change-key-name-and-remain-original-size"
	pause > nul
	
    call :execute_manual_operations "v13" "[nrd]-12-2_change-key-name-to-smaller-size"
    call :execute_manual_operations "v15" "[nrd]-12-2_change-key-name-to-smaller-size"
    pause > nul
	
    call :execute_manual_operations "v13" "[nrd]-13-2_change-key-name-to-larger-size"
    call :execute_manual_operations "v15" "[nrd]-13-2_change-key-name-to-larger-size"
    pause > nul
	
    call :execute_manual_operations "v13" "[nrd]-14-2_change-value-name-and-remain-original-size"
    call :execute_manual_operations "v15" "[nrd]-14-2_change-value-name-and-remain-original-size"
    pause > nul
	
    call :execute_manual_operations "v13" "[nrd]-15-2_change-value-name-to-smaller-size"
    call :execute_manual_operations "v15" "[nrd]-15-2_change-value-name-to-smaller-size"
    pause > nul
	
    call :execute_manual_operations "v13" "[nrd]-16-2_change-value-name-to-larger-size"
    call :execute_manual_operations "v15" "[nrd]-16-2_change-value-name-to-larger-size"
    	
	goto :end_process
		
::-----------------------------------------------------------------------------------------------
:execute_manual_operations
echo   ^-----------------------------------------------------------------------------------------
echo   == Execute manual operations %~1
echo      ^|
	    
    for /f "tokens=1 delims=_" %%i in ("%~2") do (set prefix=%%i)
    set target_hive=!prefix!_%~1.hive
	set target_outdir="%base_outdir%%~2_%~1"
	echo      ^|^--- %~2
	
    :: copy all-in-one hive to target_hive	
    copy %all_in_one_hive%_%~1.hive !target_hive! > nul
    
	:: Load the target hive file
	call :load_hive !target_hive! %~1
	
	:: open RegEdit.exe
	reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Applets\Regedit /v LastKey /t REG_SZ /d Computer\HKEY_LOCAL_MACHINE\ROOT /f > nul 2>&1
	start regedit
	
	:: wait until completing manual operations
    echo      ^|    ^|^--- Do manual operations, and then press ENTER to continue...
    pause > nul
	
	:: terminate RegEdit.exe
	taskkill /f /im regedit.exe > nul
	timeout /t 1 /nobreak > nul
	
	:: Unload the hive file
	call :unload_hive
	call :duplicate_result_files !target_outdir! !target_hive!*
    
    if exist !target_hive! (del /a !target_hive!*)
	exit /b

::-----------------------------------------------------------------------------------------------
:load_hive
	echo      ^|    ^|^--- Load the hive %~1
	:: if %~1 does not exist, reg.exe tries to create it
	reg load HKLM\ROOT "%~1" > nul 2>&1
	REM timeout /t 1 /nobreak > nul
	exit /b

:unload_hive
	echo      ^|    ^|^--- Unload the hive
	reg unload HKLM\ROOT > nul 2>&1
	REM timeout /t 1 /nobreak > nul	
	exit /b

:duplicate_result_files
	echo      ^|    ^|^--- Duplicate result files %~2
	:: copy all registry related files
	robocopy "." "%~1" "%~2" > nul 2>&1
	:: unset hidden properties
	attrib -s -h "%~1\*" > nul 2>&1
	exit /b
    
::-----------------------------------------------------------------------------------------------
:admin
	echo.
	echo.
	echo     You should run this script as administrator.
	echo.
	echo.
	pause
	exit /b
	
:end_process
	exit /b

endlocal
:: end of this script