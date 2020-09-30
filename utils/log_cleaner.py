import os


class LogCleaner:
    def __init__(self):
        """
        Log cleaner it's a tool to easy clean the log_file directory.
        To use it, just use the LogCleaner().clean()
        """
        self.path = '/'.join(os.path.abspath(__file__).split('/')[:-2])

    def clean(self):
        """
        Execute the remove command to remove *.log files into log_files/.
        :return:
        """
        try:
            cmd = f'cd {self.path} && rm -rf -v log_files/*'
            print(cmd)
            os.system(cmd)
        except PermissionError:
            raise PermissionError("Try run again as superuser.")


if __name__ == '__main__':
    LogCleaner().clean()
