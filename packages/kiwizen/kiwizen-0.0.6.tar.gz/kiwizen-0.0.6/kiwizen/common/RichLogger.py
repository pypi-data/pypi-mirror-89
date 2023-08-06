#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Copyright (c) RVBUST, Inc - All rights reserved.

import datetime
import logging
import os
import time


class RichLogger:
    __instance = None
    __LOGGER_FILE_PATH = "{}/.Logger/log_{}.log".format(
        os.getenv("HOME"), datetime.datetime.now().strftime("%Y-%m-%d__%H_%M_%S"))
    __LOGGER_FORMATTER_VERBOSE = "%(asctime)s %(name)s %(pathname)s:%(lineno)d:%(funcName)s - %(levelname)s: %(message)s"
    __LOGGER_FORMATTER_SIMPLE = "%(asctime)s %(name)s %(filename)s:%(lineno)d %(levelname)s: %(message)s"

    logger_file = ""
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARN = logging.WARN
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL

    SIMPLE = 0
    VERBOSE = 1

    def __init__(self, out_log_path=None, file_log_level=DEBUG, console_log_level=INFO, fmt=SIMPLE):
        """
        Initialize the singleton logger
        Args:
            out_log_path (str, optional): [description]. Defaults to "~/.Logger/log_[time].log".
            file_log_level (int, optional): [description]. Defaults to logging.DEBUG.
            console_log_level (int, optional): [description]. Defaults to logging.INFO.
            format (str, optional): "Verbose" or "Simple". Defaults to "Verbose".
        """
        LOGGER_FORMATTER = __class__.__LOGGER_FORMATTER_VERBOSE if fmt == self.VERBOSE else __class__.__LOGGER_FORMATTER_SIMPLE
        if out_log_path is None:
            out_log_path = __class__.__LOGGER_FILE_PATH
        os.makedirs(os.path.dirname(out_log_path), exist_ok=True)
        logging.basicConfig(level=file_log_level,
                            format=LOGGER_FORMATTER,
                            datefmt='%Y-%m-%d %H:%M:%S',
                            filename=out_log_path,
                            filemode='a')
        __class__.logger_file = out_log_path
        try:
            import coloredlogs
            coloredlogs.install(logger=logging.getLogger(""),
                                level=console_log_level,
                                fmt=LOGGER_FORMATTER,
                                datefmt='%Y-%m-%d %H:%M:%S',
                                milliseconds=False)
        except ImportError:
            logging.warning("coloredlogs is not installed")
            console_logger = logging.StreamHandler()
            console_logger.setLevel(console_log_level)
            console_logger.setFormatter(logging.Formatter(
                LOGGER_FORMATTER, datefmt='%Y-%m-%d %H:%M:%S'))
            logging.getLogger('').addHandler(console_logger)
        logging.debug(f"Logger file is set to {out_log_path}")
        __class__.__instance = self

    @ staticmethod
    def get_logger(name, level=logging.INFO):
        if __class__.__instance is None:
            __class__.__instance = RichLogger()
        logger = logging.getLogger(name)
        logger.setLevel(level)
        return logger


if __name__ == "__main__":
    def Test():
        RichLogger(fmt=RichLogger.SIMPLE, console_log_level=RichLogger.DEBUG)
        logger1 = RichLogger.get_logger('RVTApp', level=RichLogger.DEBUG)
        logger2 = RichLogger.get_logger('RVSApp')
        logger1.debug('There is a monkey.')
        logger1.info('There is human.')
        RichLogger(fmt=RichLogger.VERBOSE, console_log_level=RichLogger.DEBUG)
        logger2.debug("It's bad!")
        logger2.warning('Human kills.')
        logger2.error('Human beings are equal?')
        logger2.fatal("It is the end of human world!")

    Test()
