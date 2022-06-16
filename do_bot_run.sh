#!/bin/bash
sshpass -p 'Aa123456' ssh pi@192.168.0.42 'cd Desktop/ && export DISPLAY=:0 && ./simon.sh'
#scp pi@192.168.0.42:/Desktop/simon-py/port.txt /Desktop