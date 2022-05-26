import os


class LogCleaner:
    def __init__(self):
        self.path = '/'.join(os.path.abspath(__file__).split('/')[:-2])

    def clean(self):
        try:
            cmd = 'cd %s && rm -rf -v log_files/*' % self.path
            print(cmd)
            os.system(cmd)
        except PermissionError:
            raise PermissionError("Try run again as superuser.")


if __name__ == '__main__':
    LogCleaner().clean()
