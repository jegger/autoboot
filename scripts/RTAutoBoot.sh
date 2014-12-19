#!/bin/bash
#-------------------
# by RENTOUCH
# Dominique Burnand
#-------------------
# Script to start Screen everyday from itself.

echo "-----------------------RTAutoBoot.sh-----------------------"
LANG=en_US

#Get base directory
filepath=/home/rentouch/apps/autoboot/database.sqlite
echo "Path:" $filepath
if [ ! -f $filepath ]; then
    echo "File not found!, leaving"
    exit
fi

#get next day that is not stay_off and is not today
day_next_DB=`date +%a -d '+ 1 day'`
stay_off=$(sqlite3 $filepath 'select stay_off FROM time WHERE day="'$day_next_DB'"')
echo $stay_off
echo $day_next_DB

i=0
while [ $stay_off -eq 1 ]
do
	#Count +1 for i and get correct day-name
	i=`expr $i + 1`
	day_next_DB=`date +%a -d '+ '$i' day'`

	#check in DB if day is also a "stay_off = 1" day. Is it, it will go again trugh while
	stay_off=$(sqlite3 $filepath 'select stay_off FROM time WHERE day="'$day_next_DB'"')

	#If no of those days are a "stay_off=0" then go out and do nothing.
	echo $i
	if [ $i -eq 7 ]
		then stay_off=0
	fi
done

#If i=0 make i=1. (If tomorrow is not a "stay_off day"
if [ $i -eq 0 ]
	then i=1
fi

#Get day/time/year for next date:
day_next=`date +%d -d '+ '$i' day'`
month_next=`date +%m -d '+ '$i' day'`
year_next=`date +%Y -d '+ '$i' day'`
day_next_DB=`date +%a -d '+ '$i' day'`

#Get day/time/year for today:
day_today_DB=`date +%a`
day_today=`date +%d `
month_today=`date +%m`
year_today=`date +%Y`
TIMEZONE=`date '+%Z'`

start_hour_next=$(sqlite3 $filepath 'select start_hour FROM time WHERE day="'$day_next_DB'"')
start_min_next=$(sqlite3 $filepath 'select start_min FROM time WHERE day="'$day_next_DB'"')
start_hour_today=$(sqlite3 $filepath 'select start_hour FROM time WHERE day="'$day_today_DB'"')
start_min_today=$(sqlite3 $filepath 'select start_min FROM time WHERE day="'$day_today_DB'"')

#Write start time into var 
time_start_today=$start_hour_today":"$start_min_today":00"
time_start_next=$start_hour_next":"$start_min_next":00"
echo $time_start_today
echo $time_start_next

#Get it in EpochUTC!
epochUTC_now=`date '+%s'`
epochUTC_today=`date -u --date "$time_start_today $year_today-$month_today-$day_today $TIMEZONE" +%s`
epochUTC_next=`date -u --date "$time_start_next $year_next-$month_next-$day_next $TIMEZONE" +%s`
echo "--IN UTC (epoche)--"
echo today: $epochUTC_today -//- `date -u --date "$time_start_today $year_today-$month_today-$day_today $TIMEZONE"`
echo now:__ $epochUTC_now -//- `date -d @$epochUTC_now`
echo next:_ $epochUTC_next -//- `date -u --date "$time_start_next $year_next-$month_next-$day_next $TIMEZONE"`

#Start today or next?
stay_off_today=$(sqlite3 $filepath 'select stay_off FROM time WHERE day="'$day_today_DB'"')

if [ $stay_off_today -eq 1 ]; then 
	date_boot=$epochUTC_next
else
	check_if=$(echo  "$epochUTC_now <  $epochUTC_today" | bc)
	if [ $check_if = 1 ]
		then date_boot=$epochUTC_today
		else date_boot=$epochUTC_next
	fi
fi

#Write into system RTC
echo 0 > /sys/class/rtc/rtc0/wakealarm
echo $date_boot > /sys/class/rtc/rtc0/wakealarm
cat /sys/class/rtc/rtc0/wakealarm > /var/log/last_known_wakeup_time

echo "Next time to start"
echo $date_boot "--" `date -d @$date_boot`
