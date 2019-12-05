import logging


class Logging:
    def __init__(self, **kwargs):
        self.str_form = "%(asctime)s  %(name)s %(levelname)s %(message)s"
        try:
            if 'filename' not in kwargs:
                raise ValueError('filename must be specified')
            if 'path' in kwargs:
                filename = kwargs.pop('path') + kwargs.pop('filename')
            else:
                filename = kwargs.pop('filename')
            if 'log' not in kwargs:
                raise ValueError('log must be specified at the script\'s parameters')
            self.is_log = kwargs.pop('log')
            if not self.is_log:
                print('Disabling logs...')
            logging.basicConfig(filename=filename, format=self.str_form)
            self.logger = None

        except FileNotFoundError:
            print('No such file or directory: %s' % filename)
            exit(0)

    def log(self, msg, lvl, flag=None):
        if flag and self.is_log:
            if lvl is 'debug':
                self.logger.debug(msg)
            elif lvl is 'info':
                self.logger.info(msg)
            elif lvl is 'warn':
                self.logger.warn(msg)
            elif lvl is 'error':
                self.logger.error(msg)
            elif lvl is 'critical':
                self.logger.critical(msg)

    def config_log(self, logger_name):
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(level=logging.DEBUG)
        ch = logging.StreamHandler()
        ch.setLevel(level=logging.DEBUG)
        formatter = logging.Formatter(self.str_form)
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)
