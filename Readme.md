# Get scripts
```commandline
git clone https://github.com/Yohai1309/simon-controller
cd simon-controller
```

# Running game on Pi
Connect to the same router of the PI.

open terminal and run 
```
./do_bot_run.sh
```
OR type:
```commandline
ssh pi@192.168.0.42 'cd Desktop/ && export DISPLAY=:0 && ./simon.sh'
```
with password Aa123456

**(Please do not alter the code on the PI)**

# Controlling Simon game
open `simon_controller.py` and change port to what is written on the pi screen

open terminal and run 
```
python3 ./simon_controller.py
```

There are 4 different types of messages to send:
*   'K' - Success (continuing to the next shape)
*   'F' - Failure (restarting level)
*   'R' - Restart (restarting game)
*   'Q' - Quit (quiting game)
