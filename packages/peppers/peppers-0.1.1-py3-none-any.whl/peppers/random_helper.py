# -*- coding: utf-8 -*-

# file: random_helper.py
# date: 2020-12-17


import sys 
import random
import string


def random_int(min_val: int=None, max_val: int=None) -> int:
    if min_val is None:
        min_val = -sys.maxsize - 1
    if max_val is None:
        max_val = sys.maxsize

    return random.randint(min_val, max_val)


def random_str(length: int=32) -> str:
    random_pool = string.ascii_letters + string.digits
    return "".join(random.sample(random_pool, length))



