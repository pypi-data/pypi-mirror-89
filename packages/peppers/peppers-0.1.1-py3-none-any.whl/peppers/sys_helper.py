# -*- coding: utf-8 -*-

# file: sys_helper.py
# date: 2020-12-17


import os


def get_sys() -> str:
    return os.popen("uname -s").read().strip('\n')

