


# [S]oftware [D]efined [V]ehicular [A]d-hoc [NET]work

This project contains experiments using the concept of Software Defined Network and combines with the concept of Vehicular Ad-hoc Network to improve the communication between the network nodes.

## Prerequisites
 - Linux System's
 - [Mininet-WiFi](https://github.com/intrig-unicamp/mininet-wifi)
 - [Simulation of Urban MObility](https://www.eclipse.org/sumo/)
 

## Getting Started
 ```bash
 ~/sdvantes$ pip install -r requirements.txt
 ```
Before you run the commands below, see more about [setting up the scenario](sumo_files/README.md) and [how to use the agent](network_agent/README.md).
After all, if that is your first try, you'll need to setup the mininet's sumo scenario,
by running the following command:

```bash
~/sdvanets$ sudo python -m sdvanets --set-sumo=1 -c
```

After, you just need to run this command:
```bash
~/sdvanets$ sudo python -m sdvanets 
```
