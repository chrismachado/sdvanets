# :cop: Agents
The main idea is have an intelligence inside car, and this intelligence can be used to serve us with however information 
we want and we need. The agent can send any type of information.


## :blue_car: Vehicle Agent
This agent run inside a vehicle. He can broadcast beacon messages for his neighbors, request or response some specific 
information.

## :traffic_light: RSU Agent
This agent run inside a RSU. Its function is to communicate with the controller by updating it on the state of the road. 

### Usage
```bash
~/sdvantes$ sudo python -m network_agent -h
usage: agent.py [-h] [--log] [-s] [-n] [-r] [-m] [-e] [-d] [-w] [-c] [--filename [FILENAME]] [--filetime [FILETIME]] 
[--path [PATH]] [--name [NAME]] [--rsu] [--verbose]

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
--filetime [FILETIME] Pass the time format to be appended in filename. (e.g) python -m network_agent --log --filetime %Y --filename=foo 
                      this command will result in the name: foo2020.log
--path [PATH]         If you want your won root path for save log files
--name [NAME]         Define name of agent (should be same of the car)
--rsu                 Set the agent to be a RSU
--verbose             Allow the agent to send verbose messages

```

### Examples

Running the command below, you can see the file result example.log in log_files directory.
```bash
~/sdvantes$ sudo python agent.py --log -srnm --filename=example --name=example --verbose
```

### Log formats

The format of an agent's log is simple, but it will depend of the parameters you've choose. We have some examples in 
log_files directory, in our example, we've used the flags -srnm --verbose

```log
2020-09-26 20:23:45,754  rsu1 INFO Total received packets at iteration 24 : 63
2020-09-26 20:23:45,779  rsu1 INFO New neighbor MAC: 02:00:00:00:0f:00 | IP: 192.168.1.8
2020-09-26 20:23:45,779  rsu1 INFO Neighbors 3.
2020-09-26 20:23:45,780  rsu1 INFO Device rsu1 rebroadcast packet data b'code=18,name=car8,id=car8-25,n=0,t=1601162623.5860639' 
2020-09-26 20:23:45,848  rsu1 INFO new update message received b'code=18,name=car8,id=car8-25,n=0,t=1601162623.5860639'
```
### Agents codes
To identify which agent is running, specific codes are used for each.
```python
Agent.AGENT_CODE = 0x10
RSUAgent.AGENT_CODE = 0x11
VehicleAgent.AGENT_CODE = 0x12
```

