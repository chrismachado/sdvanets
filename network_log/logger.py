import logging
import os


class Logging:
    def __init__(self, **kwargs):
        """
        Logger tool to register all the information into the vehicles and rsus.
        :param kwargs: filename: string name of file
                       path: string path to the folder
                       log: bool to register or not the info
        """
        self.str_form = "%(asctime)s  %(name)s %(levelname)s %(message)s"
        self.__rm_privileges = dict()
        filename = ''
        try:
            if 'filename' not in kwargs:
                raise ValueError('filename must be specified')
            if 'path' in kwargs:
                self.path = kwargs.pop('path')
                filename = self.path + kwargs.pop('filename')
            else:
                filename = kwargs.pop('filename')
            if 'log' not in kwargs:
                raise ValueError('log must be specified at the script\'s parameters')
            self.is_log = kwargs.pop('log')
            if not self.is_log:
                print('Logs was disabled')
            logging.basicConfig(filename=filename, format=self.str_form)
            self.logger = None

        except PermissionError:
            raise PermissionError('Permission denied, try with sudo.')

        except IOError:
            raise IOError('No such file or directory: %s' % filename)

    def log(self, msg, lvl, flag=None):
        """
        Write the message into the log file.
        :param msg: Message received from rsu or vehicle
        :param lvl: type of log
        :param flag: bool to log specific info
        :return:
        """
        if flag and self.is_log:
            if lvl == 'debug':
                self.logger.debug(msg)
            elif lvl == 'info':
                self.logger.info(msg)
            elif lvl == 'warn':
                self.logger.warn(msg)
            elif lvl == 'error':
                self.logger.error(msg)
            elif lvl == 'critical':
                self.logger.critical(msg)

    def config_log(self, logger_name):
        """
        Configure all log features.
        :param logger_name: define name to the log.
        :return:
        """
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(level=logging.DEBUG)

        ch = logging.StreamHandler()
        ch.setLevel(level=logging.DEBUG)
        formatter = logging.Formatter(self.str_form)
        ch.setFormatter(formatter)

        self.logger.addHandler(ch)

    def set_str_form(self, str_form):
        """
        Change the string format of the log
        :param str_form: new string format
        :return:
        """
        self.str_form = str_form

    def do_runtime_packets(self, agent):
        """
        Register the runtime packets received from the vehicle or rsu
        :param agent: VehicleAgent or RSUAgent
        :return:
        """
        if agent.agent_name not in self.__rm_privileges:
            self.__rm_privileges.update([(agent.agent_name, False)])

        if self.path:
            try:
                if not os.path.exists(self.path + 'runtime_packets'):
                    os.mkdir(self.path + 'runtime_packets')

                filename = self.path + 'runtime_packets/%s_runtime.log' % agent.agent_name
                with open(filename, 'w+') as f:
                    f.write("CODE: %d | NAME: %s\n" % (agent.AGENT_CODE, agent.agent_name))
                    for key, value in agent.runtime_packets.items():
                        f.write("%s: %d\n" % (key, value))

                if not self.__rm_privileges[agent.agent_name]:
                    self.__rm_privileges[agent.agent_name] = True
                    os.system("chmod -R 777 %s" % filename)

                print("Logging runtime packets")

            except FileNotFoundError:
                raise FileNotFoundError("File not found.")
