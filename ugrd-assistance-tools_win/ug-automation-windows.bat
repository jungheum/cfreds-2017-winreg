@echo off
setlocal enabledelayedexpansion
title NIST CFReDS - User-Generated Reference Registry Generator in Windows Environment
bcdedit /enum bootmgr > nul || goto :admin

::-----------------------------------------------------------------------------------------------
goto comment
	* Description
		Automation script for creating user-generated reference registry hives 
		in Windows environment
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
		Python 2.7.9 (assume that the installation path is "c:\python27\python.exe")
		Python 3.4.3 (assume that the installation path is "c:\python34\python.exe")
:comment

echo.
echo  * User-Generated Reference Registry Hive File Generator in Windows Environment
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
	:: get the current local date & time
	for /f "usebackq tokens=1,2 delims==" %%i in (`wmic os get LocalDateTime /VALUE 2^>nul`) do (
		if '.%%i.'=='.LocalDateTime.' set ldt=%%j
	)
	set timestamp=%ldt:~0,4%-%ldt:~4,2%-%ldt:~6,2% %ldt:~8,2%.%ldt:~10,2%.%ldt:~12,2%
	set base_outdir=%~dp0[%timestamp%] User-Generated Registry Hives using WinAPI\
	mkdir "%base_outdir%"
	:: get the start time
	for /f "tokens=1-4 delims=:.," %%a in ("%time%") do (
	   set /a "time_start=(((%%a*60)+1%%b %% 100)*60+1%%c %% 100)*100+1%%d %% 100"
	)

::-----------------------------------------------------------------------------------------------		
:job_manager
	:: generate reference hive files with the format v1.3
	call :execute_nr_scripts_for_creating_each_test_case "v13"
	call :execute_nr_scripts_for_creating_a_single_all-in-one_hive "v13"
	call :execute_nrd_scripts_for_creating_each_test_case "v13"
	call :execute_cr_scripts_for_creating_each_test_case "v13"
	call :execute_mr_scripts_for_creating_each_test_case "v13"
	
	:: generate reference hive files with the format v1.5
	call :execute_nr_scripts_for_creating_each_test_case "v15"
	call :execute_nr_scripts_for_creating_a_single_all-in-one_hive "v15"
	call :execute_nrd_scripts_for_creating_each_test_case "v15"
	call :execute_cr_scripts_for_creating_each_test_case "v15"
	call :execute_mr_scripts_for_creating_each_test_case "v15"
	
	goto :end_process
		
::-----------------------------------------------------------------------------------------------
:execute_nr_scripts_for_creating_each_test_case
echo   ^-----------------------------------------------------------------------------------------
echo   == Execute 'NR' scripts for creating each test case on the format %~1
echo      (NR means normal registry hives)
echo      ^|

	for %%g in ([nr]-*.reg) do (
		set target_script=%%~nxg
		set target_outdir="%base_outdir%!target_script:~0,-4!_%~1"
		for /f "tokens=1 delims=_" %%i in ("!target_script!") do (set prefix=%%i)
		set target_hive=!prefix!_%~1.hive
		echo      ^|^--- !target_script!
		
		call :load_hive !target_hive! %~1
		call :launch_reg_script !target_script!
		call :unload_hive
		call :duplicate_result_files !target_outdir! !target_hive!*
		REM call :duplicate_result_files !target_outdir! !target_hive!

		if exist !target_hive! (del /a !target_hive!*)
	)
	
	exit /b

::-----------------------------------------------------------------------------------------------
:execute_nr_scripts_for_creating_a_single_all-in-one_hive
echo   ^-----------------------------------------------------------------------------------------
echo   == Execute 'NR' scripts for creating a single all-in-one hive on the format %~1
echo      ^|
	
	set target_hive=%all_in_one_hive%_%~1.hive
	set target_outdir="%base_outdir%!target_hive:~0,-5!"
	echo      ^|^--- Launch all NR scripts
	
	call :load_hive !target_hive! %~1
	
	for %%g in ([nr]-*.reg) do (
		set target_script=%%~nxg
		call :launch_reg_script !target_script!
	)
	
	call :unload_hive
	call :duplicate_result_files !target_outdir! !target_hive!*
	REM call :duplicate_result_files !target_outdir! !target_hive!
	
	exit /b

::-----------------------------------------------------------------------------------------------
:execute_nrd_scripts_for_creating_each_test_case
echo   ^-----------------------------------------------------------------------------------------
echo   == Execute 'NRD' scripts for creating each test case on the format %~1
echo      (NRD means normal registry hives with deleted registry data)
echo      ^|

	for %%g in ([nrd]-*.reg) do (
		set target_script=%%~nxg
		set target_outdir="%base_outdir%!target_script:~0,-4!_%~1"
		for /f "tokens=1 delims=_" %%i in ("!target_script!") do (set prefix=%%i)
		set target_hive=!prefix!_%~1.hive
		echo      ^|^--- !target_script!
		
		:: copy all-in-one hive to target_hive	
		copy %all_in_one_hive%_%~1.hive !target_hive! > nul
			
		call :load_hive !target_hive! null
		call :launch_reg_script !target_script!
		call :unload_hive
		call :duplicate_result_files !target_outdir! !target_hive!*
		REM call :duplicate_result_files !target_outdir! !target_hive!
		
		if exist !target_hive! (del /a !target_hive!*)
	)
	
	for %%g in ([nrd]-*.ps1) do (
		set target_script=%%~nxg
		set target_outdir="%base_outdir%!target_script:~0,-4!_%~1"
		for /f "tokens=1 delims=_" %%i in ("!target_script!") do (set prefix=%%i)
		set target_hive=!prefix!_%~1.hive
		echo      ^|^--- !target_script!
		
		:: copy all-in-one hive to target_hive
		copy %all_in_one_hive%_%~1.hive !target_hive! > nul
			
		call :load_hive !target_hive! null
		call :launch_ps_script !target_script!
		call :unload_hive
		call :duplicate_result_files !target_outdir! !target_hive!*
		REM call :duplicate_result_files !target_outdir! !target_hive!
		
		if exist !target_hive! (del /a !target_hive!*)
	)
	
	exit /b
	
::-----------------------------------------------------------------------------------------------
:execute_cr_scripts_for_creating_each_test_case
echo   ^-----------------------------------------------------------------------------------------
echo   == Execute 'CR' scripts for creating each test case on the format %~1
echo      (CR means corrupted registry hives)
echo      ^|

	for %%g in ([cr]-*.py) do (
		set target_script=%%~nxg
		set target_outdir="%base_outdir%!target_script:~0,-3!_%~1"
		for /f "tokens=1 delims=_" %%i in ("!target_script!") do (set prefix=%%i)
		set target_hive=!prefix!_%~1.hive
		echo      ^|^--- !target_script!
		
		:: copy all-in-one hive to target_hive	
		copy %all_in_one_hive%_%~1.hive !target_hive! > nul
			
		call :launch_python_script_34 !target_script! !target_hive!
		call :duplicate_result_files !target_outdir! !target_hive!*
		REM call :duplicate_result_files !target_outdir! !target_hive!*
		
		if exist !target_hive! (del /a !target_hive!*)
	)	

	exit /b

::-----------------------------------------------------------------------------------------------
:execute_mr_scripts_for_creating_each_test_case
echo   ^-----------------------------------------------------------------------------------------
echo   == Execute 'MR' scripts for creating each test case on the format %~1
echo      (MR means manipulated registry hives)
echo      ^|

	for %%g in ([mr]-*.py) do (
		set target_script=%%~nxg
		set target_outdir="%base_outdir%!target_script:~0,-3!_%~1"
		for /f "tokens=1 delims=_" %%i in ("!target_script!") do (set prefix=%%i)
		set target_hive=!prefix!_%~1.hive
		echo      ^|^--- !target_script!
		
		:: copy all-in-one hive to target_hive	
		copy %all_in_one_hive%_%~1.hive !target_hive! > nul
					
		if "!prefix!" == "[mr]-15" (
			REM ::--------------------------------------------------------
			REM :: for adding reg items to the base hive file with all types of NR category
			REM ::--------------------------------------------------------
			call :load_hive !target_hive! null
			
			:: call a script within the python 2.7 environment
			call :launch_python_script_27 !target_script! !target_hive!
		
			:: for adding reg items in the case of different-encodings
			call :unload_hive
			call :duplicate_result_files !target_outdir! !target_hive!*
			REM call :duplicate_result_files !target_outdir! !target_hive!
		) else (
			REM ::--------------------------------------------------------
			REM :: for modifying the base hive file with all types of NR category
			REM ::--------------------------------------------------------
			call :launch_python_script_34 !target_script! !target_hive!
		
			call :duplicate_result_files !target_outdir! !target_hive!*
			REM call :duplicate_result_files !target_outdir! !target_hive!*
		)
				
		if exist !target_hive! (del /a !target_hive!*)
	)
		
	exit /b

::-----------------------------------------------------------------------------------------------
:load_hive
	echo      ^|    ^|^--- Load the hive %~1
	:: if %~1 does not exist, reg.exe tries to create it
	reg load HKLM\ROOT "%~1" > nul 2>&1
	REM timeout /t 1 /nobreak > nul
	if "%~2" == "v15" (
		call :unload_hive
		echo      ^|    ^|^--- Patch the current hive format from v1.3 to v1.5
		python "cftt_regf_v1.3_to_v1.5.py" "%~1"  > nul 2>&1
		call :load_hive %~1 null
	)
	exit /b

:unload_hive
	echo      ^|    ^|^--- Unload the hive
	reg unload HKLM\ROOT > nul 2>&1
	REM timeout /t 1 /nobreak > nul	
	exit /b

:launch_reg_script
	echo      ^|    ^|^--- Launch the .REG script %~1
	regedit.exe /s %~1  > nul 2>&1
	REM timeout /t 1 /nobreak > nul		
	exit /b	
	
:launch_ps_script
	echo      ^|    ^|^--- Launch the PowerSehll script %~1
	Powershell.exe -noprofile -executionpolicy bypass -file ".\%~1"  > nul 2>&1
	REM timeout /t 1 /nobreak > nul		
	exit /b	
	
:launch_python_script_27
	echo      ^|    ^|^--- Launch the Python script %~1
	c:\python27\python.exe "%~1" "%~2" > nul 2>&1
	REM timeout /t 1 /nobreak > nul
	exit /b		
	
:launch_python_script_34
	echo      ^|    ^|^--- Launch the Python script %~1
	c:\python34\python.exe "%~1" "%~2" > nul 2>&1
	REM c:\python34\python.exe "%~1" "%~2" > nul 2>&1
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
	if exist *%all_in_one_hive%*.hive (del /a *%all_in_one_hive%*)
	
	:: get the end time
	for /f "tokens=1-4 delims=:.," %%a in ("%time%") do (
	   set /a "time_end=(((%%a*60)+1%%b %% 100)*60+1%%c %% 100)*100+1%%d %% 100"
	)	
	:: show the elapsed time
	set /a elapsed=time_end-time_start
	set /a hh=elapsed/(60*60*100), r=elapsed%%(60*60*100), mm=r/(60*100), r%%=60*100, ss=r/100
	if %hh% lss 10 set hh=0%hh%
	if %mm% lss 10 set mm=0%mm%
	if %ss% lss 10 set ss=0%ss%
	echo   ^-----------------------------------------------------------------------------------------
	echo   Time taken %hh%:%mm%:%ss%
	exit /b

endlocal
:: end of this script