import logging
from logging import log
import os
from datetime import datetime

dir_path = 'D:\\Users\\Administrator\\gb5566\\yahoo_ptt\\logger\\logs\\'
filename = "{:%Y-%m-%d}".format(datetime.now()) + '.log'

def create_logger(log_folder):
    # congif
    logging.captureWarnings(True) # capture Warnings message
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    my_logger = logging.getLogger('py.warnings')
    my_logger.setLevel(logging.INFO)

    if not os.path.exists(dir_path + log_folder):
        os.makedirs(dir_path + log_folder)

    # file handler
    fileHandler = logging.FileHandler(dir_path+log_folder+'\\'+filename, 'w', 'utf-8')
    fileHandler.setFormatter(formatter)
    my_logger.addHandler(fileHandler)

    # console handler
    consoleHandler = logging.StreamHandler()
    consoleHandler.setLevel(logging.DEBUG)
    consoleHandler.setFormatter(formatter)
    my_logger.addHandler(consoleHandler)

    return my_logger