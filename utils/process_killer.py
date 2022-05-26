import os
import subprocess
import signal


class ProcessKiller:
    def __init__(self, expression):
        self.expression = expression

    def stop(self):
        process_list = self.get_process_list()

        if not process_list:
            print('No process with expression \'{%s}\' was found.' % self.expression)
            return

        try:
            print('Trying to kill the process...')
            if len(process_list) <= 2:
                print('Process list is empty.')

            for process in process_list[:-2]:
                print('\tKilling process {%s}' % process)
                os.kill(int(process[0]), signal.SIGKILL)

        except PermissionError:
            raise PermissionError('Try again with sudo')

        except ProcessLookupError:
            raise ProcessLookupError('Can\'t find the process {%s}' % process[0])

    def get_process_list(self):
        ps = subprocess.Popen('ps -ax | grep -E \'{%s}\'' % self.expression,
                              stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE,
                              shell=True)

        outs, err = ps.communicate()

        if err:
            raise Exception('Error has occurred')

        outs = outs.decode('utf-8').split('\n')
        out_str = []
        for out in outs:
            out_aux = []
            for _out in out.strip().split(' '):
                if _out != '' and _out != []:
                    out_aux.append(_out)

            if out_aux:
                out_str.append(out_aux)

        return out_str


if __name__ == '__main__':
    expression = 'python2.7|mininet|scenario|poxcontroller|mininet-wifi'
    ProcessKiller(expression=expression).stop()
