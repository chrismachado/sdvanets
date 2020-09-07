# :cop: Agents
The main idea is have an intelligence inside car, and this intelligence can be used to serve us with however information we want and we need. The agent can send any type of information.


## :blue_car: Vehicle Agent
This agent run inside an vehicle. He can broadcast messages for his neighbors with some special informations.

### Usage
```bash
~/sdvantes$ sudo python agent.py -h
usage: agent.py [-h] [--log] [-s] [-n] [-r] [-m] [-e] [-d] [-w] [-c] [--filename [FILENAME]] [--filetime [FILETIME]] [--path [PATH]]

Sending and monitoring messages in vehicle ad-hoc network (VANET). Using flags to update the network.

optional arguments:
-h, --help            show this help message and exit
--log                 Enable log messages
-s                    Log sent messages
-n                    Log new neighbors
-r                    Log received messages
-m                    Log basic messages
-e                    Log error messages
-d                    Log debug messages
-w                    Log warning messages
-c                    Log critical messages
--filename [FILENAME] Define filename to log file
--filetime [FILETIME] Pass the time format to be appended in filename. (e.g) agent.py --log --filetime %Y
--filename test this command will result in the name: test2020.log
--path [PATH]         If you want your won root path for save log files
```

### Examples

Running the command below, you can see the file result example.log in log_files directory.
```bash
~/sdvantes$ sudo python agent.py --log -srnm --filename example
```

### Log formats

The format of an agent's log is simple, but it will depend of the parameters you've choose. We have some examples in log_files directory, in our example, we've used the flags -srnm.

```log
2020-08-04 08:40:44,673  rsu1 INFO Device rsu1 rebroadcast packet data b'{<car14-104>,position,0,1596541241.4574494}'
rebroadcast packet data b'{<car4-107>,position,0,1596541248.6373088}' 
2020-08-04 08:40:50,835  rsu1 INFO new update message received b'{<car4-107>,position,0,1596541248.6373088}'
2020-08-04 08:40:50,835  rsu1 INFO New neighbor added 02:00:00:00:1d:00
2020-08-04 08:40:50,835  rsu1 INFO Neighbors 2.
```

