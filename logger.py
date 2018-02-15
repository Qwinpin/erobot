import logging


class Log:
    def __init__(self):
        self.logger = logging.getLogger("send_log")
        self.logger.setLevel(logging.INFO)
        self.fh = logging.FileHandler("log.log")
        self.formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s - %(lineno)d'
        )
        self.fh.setFormatter(self.formatter)
        self.logger.addHandler(self.fh)

    def information(self, text):
        self.logger.info(text)

    def error(self, text):
        self.logger.error(text)
