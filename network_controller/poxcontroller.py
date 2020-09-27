import subprocess


class PoxController(object):
    def __init__(self, cmd, **kwargs):
        '''
        This class will execute the Pox Controller.
        :param cmd: A command to execute the pox, should input the path too
        :param kwargs: Arguments that should go to the pox
        '''
        self.cmd = cmd
        self.params = kwargs

    def run(self):
        self.start_pox()

    def start_pox(self):
        _cmd = self.__mount_exec_cmd()
        pox = subprocess.Popen(_cmd,
                               stdin=subprocess.PIPE,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE,
                               shell=True)
        out, err = pox.communicate()
        if err:
            raise Exception(f'Error has occurred {err}')

        print('Pox controller started.')

    def __mount_exec_cmd(self):
        '''
        Create the command to be use on the pox controller thread
        :return: string command
        '''
        _cmd = 'gnome-terminal -- ' + self.cmd
        for values in self.params.values():
            _cmd += ' ' + values

        return _cmd
