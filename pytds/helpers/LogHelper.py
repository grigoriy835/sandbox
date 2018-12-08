import logging
import os
from .Singleton import Singleton
from logging.handlers import WatchedFileHandler


class LogHelper(metaclass=Singleton):
    logPath = 'storage/logs/'
    loggers = None
    formatter = None

    def __init__(self):
        self.formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        self.loggers = {}
        # self.initLogger('aiohttp.server', 'error_log.log', logging.ERROR)
        # self.initLogger('aiohttp.access', 'access_log.log')
        self.initLogger('response_log', 'work_logs/response_log.log')
        self.initLogger('chooser_log', 'work_logs/chooser_log.log')
        self.initLogger('bonus_event_log', 'work_logs/bonus_event_log.log')
        self.initLogger('parser', 'work_logs/parser.log')
        self.initLogger('smart_rotator', 'work_logs/smart_rotator.log')
        self.initLogger('scripts_redirect_log', 'work_logs/scripts_redirect_log.log')
        self.initLogger('redirect_log', 'work_logs/redirect_log.log')

    def initLogger(self, name, log_file, level=logging.INFO):

        try:
            os.makedirs(os.path.dirname(self.logPath + log_file), exist_ok=True)
        except TypeError:
            pass

        if os.environ.get('LOG_LEVEL', 'ALL') == 'ERROR':
            level = logging.ERROR

        handler = WatchedFileHandler(self.logPath + log_file)
        handler.setFormatter(self.formatter)

        logger = logging.getLogger(name)
        logger.setLevel(level)
        logger.addHandler(handler)

        self.loggers[name] = logger

    def infoMessage(self, loggerName, message):
        if loggerName not in self.loggers:
            self.initLogger(loggerName, loggerName + '.log')

        self.loggers[loggerName].info(message)

    def getLogger(self, name):
        if name not in self.loggers:
            self.initLogger(name, name + '.log')

        return self.loggers[name]
