#!/bin/bash
sshpass -p 'Ninja@2022' ssh -o 'StrictHostKeyChecking no' -n -f simonpi@192.168.0.64 'cd Desktop/ && export DISPLAY=:0 && nohup ./simon.sh > /dev/null 2>&1 &'
sshpass -p 'Ninja@2022' ssh -o 'StrictHostKeyChecking no' -n -f simonpi@192.168.0.42 'cd Desktop/ && export DISPLAY=:0 && nohup ./simon.sh > /dev/null 2>&1 &'
sshpass -p 'Ninja@2022' ssh -o 'StrictHostKeyChecking no' -n -f simonpi@192.168.0.45 'cd Desktop/ && export DISPLAY=:0 && nohup ./simon.sh > /dev/null 2>&1 &'
sshpass -p 'Ninja@2022' ssh -o 'StrictHostKeyChecking no' -n -f simonpi@192.168.0.155 'cd Desktop/ && export DISPLAY=:0 && nohup ./simon.sh > /dev/null 2>&1 &'
