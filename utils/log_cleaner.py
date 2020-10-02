import os
from time import sleep

class LogCleaner:
    def __init__(self):
        self.path = '/'.join(os.path.abspath(__file__).split('/')[:-2])

    def log_clean(self):
        try:
            cmd = f'cd {self.path} && rm -rf -v log_files/*'
            print(f'Running {cmd}')
            os.system(cmd)
        except PermissionError:
            raise PermissionError("Try run again as superuser.")

    def mn_clean(self):
        try:
            cmd = f'cd {self.path} && mn -c'
            print(f'Running {cmd}')
            os.system(cmd)
        except PermissionError:
            raise PermissionError("Try run again as superuser.")


if __name__ == '__main__':
    cleaner = LogCleaner()
    cleaner.log_clean()
    sleep(2)  # wait to clean
    cleaner.mn_clean()
