#!/bin/bash

sleeptime=2

while true
do
	if [ $(date +%H) = 01 ] && [ $(date +%M) -lt 02 ]
	then	
		echo "its 10"
		shutdown -h now
	else
		echo "hud2"
		echo $(date +%S)
		if [ $(date +%S) -lt 09 ]
		then
			echo "thentsvv 2"
		fi
	fi
	sleep $sleeptime
done

