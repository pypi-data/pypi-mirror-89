# -*- coding: utf-8 -*-

# file: log_helper.py
# date: 2020-12-17


import logging


def get_logger(name: str, level: str="INFO", 
        format_temp: str="%(asctime)s - %(name)s - %(levelname)s - %(message)s", 
        console_level: str=None):
    format_temp = logging.Formatter(format_temp)
    logger = logging.getLogger(name)
    log_level = eval("logging.{}".format(level))
    logger.setLevel(log_level)

    console_level = \
        log_level if console_level is None else eval("logging.{}".format(console_level))
    console_handler = logging.StreamHandler()
    console_handler.setLevel(console_level)
    console_handler.setFormatter(format_temp)

    logger.addHandler(console_handler)
    return logger


# TODO: Still in expt, ref to https://foofish.net/python-decorator.html
def fn_logger_decorator(logger, loggin_temp: str="Function %s starting"):
    def decorator(func):
        def wrapper(*args, **kwargs):
            print("\n")
            logger.info(loggin_temp % func.__name__)   
            return func(*args)
        return wrapper

    return decorator


