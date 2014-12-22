#!/bin/sh
#-------------------
# by RENTOUCH
# Dominique Burnand (March,2011)
#-------------------
# Script to manage shutdown
#	

echo "-----------------------RTAutoShutDown.sh-----------------------"
LANG=en_US

#Get base directory
filepath_shutdown_time=/home/rentouch/apps/autoboot/shutdown-time.txt

#Read shut-down UTC(epoche/unix)
shutdown_time="$(cat $filepath_shutdown_time)"

#check if the screen shoudn't shut down. (value=0)
if [ $shutdown_time -eq 0 ]; then
	echo "Screen stay on today"
else
	#Convert the UTC(epoche) to UTC(epoche) rounded. Round the time to minutes
	now_time_date=`date +"%Y-%m-%d-%Z"`
	now_time_time=`date +"%H:%M"`
	time_shut_now=$now_time_time":00"
	epochUTC_now=`date -u --date "$time_shut_now $now_time_date" +%s`

	#Check if reached moment of shut-down
	echo shutdowntime: $shutdown_time "--" `date -d @$shutdown_time`
	echo time-now: $epochUTC_now "--" `date -d @$epochUTC_now`
	if [ $epochUTC_now -eq $shutdown_time ]; then
		/sbin/shutdown -h now
	fi
fi


