#coding: utf-8
from __future__ import unicode_literals, print_function

__author__='smirnov.ev'

import datetime


def str2int_safe(string):
    try:
        return int(string)
    except ValueError:
        return None


def str2float_safe(string):
    try:
        return float(string)
    except ValueError:
        return None


def str2sec_safe(string):
    # string: '4:35'
    # type: str
    # return: 210
    # type: int
    try:
        func = datetime.datetime.strptime
        return int((func(string, '%M:%S')-func('0','%S')).total_seconds())
    except:
        return None