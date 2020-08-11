# Setting Scenario
Changing the standard sumo scenario of mininet-wifi. This changing is necessary to run our scenario. 

## How to
```bash
~/sdvanets$ cd sumo_files/
~/sdvanets/sumo_files$ cp *.xml sumo.cfg PATH/mininet-wifi/mn_wifi/sumo/data/

~/sdvanets/sumo_files$ cd PATH/mininet-wifi/
~/mininet-wifi$ sudo make install
```
_note 1: PATH should be the real path to the directory mininet-wifi/ on your system_

_note 2: This scenario is syncronized with python scenario file_

Every time you change this files you need to execute the last command.

