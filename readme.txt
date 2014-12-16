_____________________________
Copyright 2012 Rentouch
Developer: Burnand Dominique
_____________________________


Installation for AutoBoot
-------------------------
1. Set time to UTC
	1. sudo hwclock --systohc --utc
	2. test this step with: sudo hwclock --debug

2. Make sure the system time is in english
	1. ?
	2. Test with: date +%a -d '+ 1 day'

3. Deactivate HPET
	1. sudo gedit /etc/default/grub
	2. add line: GRUB_CMDLINE_LINUX_DEFAULT="hpet=disable"
	2. sudo update-grub

4. Disable automatic HWClock update
	1. sudo gedit /etc/init/hwclock-save.conf
	2. comment line: exec hwclock --rtc=/dev/rtc0 --systohc $tz --noadjfile $badyear
	3. it should look now: #exec hwclock --rtc=/dev/rtc0 --systohc $tz --noadjfile $badyear
	
5. Installing Sqlite3
	1. sudo apt-get install sqlite3

6. Create cronejob
	1. sudo crontab -e
	2. Copy paste the content of file scrips/cronjob into the terminal editor
	3. Change all path to the scripts / assure all the paths are correct
	4. Look out: The last line have to be an empty line!
	5. Save (with ctrl+x)

7. Change scripts to your need (theoretically you it shuld already working)
   For this it has to be in: ~/probazaar/settings/autoboot/scripts
	1. RTAutoBoot.sh
		1. Line7 (change path to database)
	2. RTAutoShutDown.sh
		2. Line9 (change path to shutdown-time.txt)
	3. RTWriteShutDown.sh
		1. Line12 (change path to database)
		2. Line13 (change path to shutdown-time.txt)






OLD - out of date.....:
-----------------------
Autobot ubuntu10.X

- Zeit auf UTC stellen:
sudo hwclock --systohc --utc  # the hardware clock is kept in UTC
Testen mit : sudo hwclock --debug

- HPET ausschalten: 
sudo gedit /etc/default/grub
(add Linie: GRUB_CMDLINE_LINUX_DEFAULT="hpet=disable"
sudo update-grub

-Install sqlite3
sudo apt-get install sqlite3

- make cronjob:
sudo crontab -e
In File anhängen:
#-----------------------------------------------------------------
# Shell variable for cron
#SHELL=/bin/sh
# PATH variable for cron
#PATH=/usr/local/bin:/usr/local/sbin:/sbin:/usr/sbin:/bin:/usr/bin:/usr/bin/X11
#M   S     T M W   Befehl
#-----------------------------------------------------------------
*/1 *    * * *  sh /home/rentouch/workspace/RTAutoBoot.sh  2>&1 >> /var/log/checktime.log
*/1 *    * * *  sh /home/rentouch/workspace/RTWriteShutDown.sh  2>&1 >> /var/log/checktime.log
*/1 *    * * *  sh /home/rentouch/workspace/RTAutoShutDown.sh  2>&1 >> /var/log/checktime.log
#-----------------------------------------------------------------

-System-datun muss in english sein! -> Mon,Tue,Wed,Thu,Fri,Sat,Sun (testen mit: date +%a -d '+ 1 day') (für RTAutoBoot.sh)

-automatisches HWClok update deaktivieren:
sudo gedit /etc/init/hwclock-save.conf
Zeile komentieren:  #    exec hwclock --rtc=/dev/rtc0 --systohc $tz --noadjfile $badyear

as
