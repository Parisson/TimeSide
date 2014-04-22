#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging


class Logger:

    """A logging object"""

    def __init__(self, file):
        self.logger = logging.getLogger('myapp')
        self.hdlr = logging.FileHandler(file)
        self.formatter = logging.Formatter(
            '%(asctime)s %(levelname)s %(message)s')
        self.hdlr.setFormatter(self.formatter)
        self.logger.addHandler(self.hdlr)
        self.logger.setLevel(logging.INFO)

    def write_info(self, message):
        self.logger.info(message)

    def write_error(self, message):
        self.logger.error(message)
