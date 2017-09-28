#!/bin/bash
#-----------------------------------------------------------------------------------------------
# * Description
#		Automation script for creating user-generated reference registry hives 
# 		in Linux environment with Hivex (Red Hat, libguestfs.org) library
# * Author
# 		Jungheum Park (jungheum.park@nist.gov)
# * Organization
# 		Software and Systems Division
# 		Information Technology Laboratory
# 		National Institue of Standards and Technology
# 		U.S. Department of Commerce
# * Project @ NIST
# 		CFTT   (Computer Forensic Tool Testing)         www.cftt.nist.gov
# 		CFReDS (Computer Forensic Reference Data Sets)  www.cfreds.nist.gov
# * License
# 		Apache License 2.0
# * Hivex information
#		libguestfs-tools (1.32.2-4)   sudo apt-get install libguestfs-tools
#		python-hivex (1.3.13-1)         sudo apt-get install python-hivex
#       
# * Tested Environment
# 		Linux 3.18.0-kali1-amd64 #1 SMP Debian 3.18.3-1~kali4 (2015-01-22) x86_64 GNU/Linux
#		Linux 4.0.0-kali1-amd64 #1 SMP Debian 4.0.4-1+kali2 (2015-06-03) x86_64 GNU/Linux
#       Linux 4.10.0-35-generic #39~16.04.1-Ubuntu SMP Wed Sep 13 09:02:42 UTC 2017 x86_64 x86_64 x86_64 GNU/Linux
#

clear
echo
echo "   * User-Generated Reference Registry Hive File Generator in Linux Environment"
echo
echo "   * Developed and managed by"
echo "     - NIST CFTT   (Computer Forensic Tool Testing)         www.cftt.nist.gov"
echo "     - NIST CFReDS (Computer Forensic Reference Data Sets)  www.cfreds.nist.gov"
echo

#-----------------------------------------------------------------------------------------------
echo "   -----------------------------------------------------------------------------------------"
echo "   == Set global variables"
base_hive="base.hive"
all_in_one_hive="[nr]-##-2_all-in-one"
# get the current local date & time
timestamp=$(date +"%Y-%m-%d %H.%M.%S")
base_outdir="$(pwd)/[$timestamp] User-Generated Registry Hives using Hivex/"
mkdir "$base_outdir"
# get the start time
time_start=$(date +%s)

#-----------------------------------------------------------------------------------------------
delete_file()
{
	if [ -f "$1" ]; then 
		rm -rf "$1"
	fi
}

end_process() 
{
	delete_file "${all_in_one_hive}_$1.hive"
	
	# get the end time
	time_end=$(date +%s)
	
	# show the elapsed time
	elapsed=$(($time_end-$time_start))
	hh=$(($elapsed/(60*60)))
	rr=$(($elapsed%(60*60)))
	mm=$(($rr/(60)))
	rr=$(($rr%(60)))
	ss=$rr
	echo   "   -----------------------------------------------------------------------------------------"
	printf "   Time taken %02d:%02d:%02d\n" $hh $mm $ss
	exit 0
}

#-----------------------------------------------------------------------------------------------
launch_python_script()
{
	echo "      |    |--- Launch the python script $1"
	#python "$1" "$2"
	python "$1" "$2" >/dev/null 2>/dev/null
}

duplicate_result_file()
{
	echo "      |    |--- Duplicate the result file $2"
	cp $2 "$1" >/dev/null 2>/dev/null
}

#-----------------------------------------------------------------------------------------------
execute_nr_scripts_for_creating_each_test_case()
{
	echo "   -----------------------------------------------------------------------------------------"
	echo "   == Execute 'NR' scripts for creating each test case"
	echo "      (NR means normal registry hives)"
	echo "      |"
		
	for file in [nr\]-*.py ; do
		target_script=$file
		target_outdir="$base_outdir${target_script:0:-3}_$1/"
		target_hive="${target_script:0:9}_$1.hive"
		echo "      |--- $target_script"
		
		# copy base_hive to target_hive
		cp $base_hive $target_hive
		
		launch_python_script $target_script $target_hive
		
		mkdir "$target_outdir"
		duplicate_result_file "$target_outdir" $target_hive
				
		delete_file $target_hive
	done
}

#-----------------------------------------------------------------------------------------------
execute_nr_scripts_for_creating_a_single_all-in-one_hive()
{
	echo "   -----------------------------------------------------------------------------------------"
	echo "   == Execute 'NR' scripts for creating a single all-in-one hive"
	echo "      |"
	
	target_hive="${all_in_one_hive}_$1.hive"
	target_outdir="$base_outdir${target_hive:0:-5}/"
	echo "      |--- Launch all NR scripts"
	
	# copy base_hive to target_hive
	cp $base_hive $target_hive
	
	for file in [nr\]-*-2_*.py ; do
		target_script=$file		
		launch_python_script $target_script $target_hive
	done
	
	mkdir "$target_outdir"
	duplicate_result_file "$target_outdir" $target_hive
}

#-----------------------------------------------------------------------------------------------
execute_nrd_scripts_for_creating_each_test_case()
{
	echo "   -----------------------------------------------------------------------------------------"
	echo "   == Execute 'NRD' scripts for creating each test case"
	echo "      (NRD means normal registry hives with deleted registry data)"
	echo "      |"
	
	for file in [nrd\]-*.py ; do
		target_script=$file
		target_outdir="$base_outdir${target_script:0:-3}_$1/"
		target_hive="${target_script:0:10}_$1.hive"
		echo "      |--- $target_script"

		# copy base_hive to target_hive
		cp "${all_in_one_hive}_$1.hive" $target_hive
		
		launch_python_script $target_script $target_hive
		
		mkdir "$target_outdir"
		duplicate_result_file "$target_outdir" $target_hive
				
		delete_file $target_hive		
	done
}

#-----------------------------------------------------------------------------------------------
# main jobs
#
execute_nr_scripts_for_creating_each_test_case "v13"

execute_nr_scripts_for_creating_a_single_all-in-one_hive "v13"

execute_nrd_scripts_for_creating_each_test_case "v13"

end_process "v13"

# end of this script
