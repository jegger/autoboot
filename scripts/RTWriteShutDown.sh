#!/bin/sh
#-------------------
# by RENTOUCH
# Dominique Burnand (March,2011)
#-------------------
# Script to manage shutdown
#
# Write shutdown time in $filepath_shutdown_time (shutdown-time.txt)
# The time is writen in UTC-Epoch (unix) time.
# If the screen should stay on! in the file is wrote a "0"	

echo "-----------------------RTWirteShutDown.sh-----------------------"

#Get base directory
BASEDIR=$(dirname $(readlink -f $0))
filepath=$BASEDIR"/../database.sqlite"
filepath_shutdown_time=$BASEDIR"/../shutdown-time.txt"

#Get hour/min for today
day_today_DB=`date +%a`
shut_hour_today=$(sqlite3 $filepath 'select stop_hour FROM time WHERE day="'$day_today_DB'"')
shut_min_today=$(sqlite3 $filepath 'select stop_min FROM time WHERE day="'$day_today_DB'"')

#Get all timevariables
day_today=`date +%d `
month_today=`date +%m`
year_today=`date +%Y`
TIMEZONE=`date +%Z`

#format 24:00 -> 23:59:59, else let it be as it is
if [ $shut_hour_today -eq 24 -a $shut_min_today -eq 0 ]; then
	shut_hour_today_formated=23
	shut_min_today_formated=59
	shut_sec_today_formated=59
else
	shut_hour_today_formated=$shut_hour_today
	shut_min_today_formated=$shut_min_today
	shut_sec_today_formated=00
fi

#Get the shutdown in UTC (epoch)
time_shut_today=$shut_hour_today_formated":"$shut_min_today_formated":"$shut_sec_today_formated
epochUTC_today=`date -u --date "$time_shut_today $year_today-$month_today-$day_today $TIMEZONE" +%s`
#echo "EPOCH:"$epochUTC_today "--" `date -d @$epochUTC_today`

#Check if the screen should stayon while tomorrow (today 24:00=true)
if [ $shut_hour_today -eq 24 -a $shut_min_today -eq 0 ]; then 
	#now check if the next date is also stay on on 00:00
	day_tomorrow_DB=`date +%a -d '+ 1 day'`
	start_hour_tomorrow=$(sqlite3 $filepath 'select start_hour FROM time WHERE day="'$day_tomorrow_DB'"')
	start_min_tomorrow=$(sqlite3 $filepath 'select start_min FROM time WHERE day="'$day_tomorrow_DB'"')
	if [ $start_hour_tomorrow -eq 0 -a $start_min_tomorrow -eq 0 ]; then
		echo stayon!
		echo 0 > $filepath_shutdown_time
	else
		echo go off opn 24:00
		echo $epochUTC_today >  $filepath_shutdown_time
	fi
else
	echo "go off on induvidual:" `date -d @$epochUTC_today`
	echo $epochUTC_today >  $filepath_shutdown_time
fi

# Abort shutdown!
#sudo shutdown -c

#echo $stay_off
#echo $shut_hour":"$shut_min

#sudo shutdown -h $shut_hour":"$shut_min

