#!/bin/bash
sshpass -p 'Ninja@2022' ssh -o 'StrictHostKeyChecking no' -n -f simonpi@192.168.0.64 'sudo reboot'
sshpass -p 'Ninja@2022' ssh -o 'StrictHostKeyChecking no' -n -f simonpi@192.168.0.42 'sudo reboot'
sshpass -p 'Ninja@2022' ssh -o 'StrictHostKeyChecking no' -n -f simonpi@192.168.0.45 'sudo reboot'
sshpass -p 'Ninja@2022' ssh -o 'StrictHostKeyChecking no' -n -f simonpi@192.168.0.155 'sudo reboot'
