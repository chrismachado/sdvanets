import subprocess
import os
import signal

from subprocess import check_output, CalledProcessError


class PoxController(object):
    def __init__(self, cmd, **kwargs):
        '''
        This class will execute the Pox Controller.
        :param cmd: A command to execute the pox, should input the path too
        :param kwargs: Arguments that should go to the pox
        '''
        self.cmd = cmd
        self.params = kwargs
        self.ppx = None

    def run(self):
        '''
        Run the pox controller
        :return: Return the PoxController class
        '''
        self.__init_px()
        while True:
            r = self.__chooser()
            if r:
                break
        return self

    def __stop_px(self):
        '''
        Stop the main thread of pox controller
        :return: boolean for the loop
        '''
        print('Stopping pox controller')
        if self.ppx is not None:
            self.ppx.kill()
            self.ppx = None

        return False

    def __init_px(self):
        '''
        Start pox controller thread
        :return: boolean for the loop
        '''
        if self.ppx is None:
            print('Pox controller started.')
            _cmd = self.__mount_exec_cmd()
            self.ppx = subprocess.Popen(_cmd,
                                        stdin=subprocess.PIPE,
                                        stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE,
                                        shell=True)
            self.ppx.pid += 1  # fixing the correct pid for pox process
        return False

    def __mount_exec_cmd(self):
        '''
        Create the command to be use on the pox controller thread
        :return: string command
        '''
        _cmd = self.cmd
        for values in self.params.values():
            _cmd += ' ' + values

        return _cmd

    def __chooser(self):
        '''
        Allow the user to decide what he want to do
        :return: boolean for the loop
        '''
        print('Select an option: ', end=' ')
        options = {'stop': self.__stop_px,
                   'rerun': self.__rerun}

        if self.ppx is not None:
            for key in options.keys():
                print(f' {key} ', end='|')
        else:
            print(' start ', end='|')
            options.update({'start': self.__init_px})

        print(' exit')

        options.update({'exit': self.__exit})
        options.update({'kill all': self.__ultimate_kill})

        key = input()

        try:
            if key == 'kill all':
                arg = input('Select list of processes to kill? (Y/n)\n')
                return options[key](arg)
            return options[key]()
        except KeyError:
            print('> Type a correct option')
            return False

    # TODO: Usar no vehicle_agent
    def get_pid(self, name):
        '''
        Get the id of the process with name=[name]
        :param name: name of the process, e.g python
        :return: list of pids
        '''
        try:
            return map(int, check_output(['pidof', name]).split())
        except CalledProcessError:
            return []

    def __ultimate_kill(self, _all=''):
        '''
        Dev tool utility to kill all processes with defined list
        :param _all: string (Y - to select a list of process, anything - to not select)
        :return: boolean for the loop
        '''
        print('Entering the dev tool KILL_ALL')
        name = input('Give me the process name: ')
        list_to_kill = self.get_pid(name=name)
        if _all == 'Y':
            select = input('select pids: %s\n' % list(list_to_kill))
            list_to_kill = map(int, select.split(','))

        try:
            for process in list_to_kill:
                print(f'Killing process {process}')
                os.kill(process, signal.SIGKILL)

            self.ppx = None
            return False

        except ProcessLookupError:
            print('Invalid pid, try again.')
            self.__ultimate_kill(_all='Y')
            return False

    def __exit(self):
        '''
        Kill all python2.7 (pox controller version) process
        :return: boolean for the loop
        '''
        print('Exiting...')
        if self.ppx is not None:
            self.__stop_px()

        return True

    def __rerun(self):
        '''
        Create a new pox controller thread
        :return: boolean for the loop
        '''
        print('Restarting the pox controller')
        if self.ppx is not None:
            self.__stop_px()

        self.__init_px()
        return False
