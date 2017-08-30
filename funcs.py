# -*- coding: utf-8 -*-
#
#  funcs.py
#  
#  Copyright 2017 Vladimir Adamsky <vladimiradamsky@gmail.com>
#  
#  Functions from this file uses in ProcessController class.
#  
#  
import time
import random
import logging


def func(mu, sigma):
    """Calculate of sleeping time by normal distribution 
    and sleep it
    """
    logger = logging.getLogger("func")
    dt = max(0, random.normalvariate(mu, sigma))
    logger.info("func will sleep %f seconds", dt)
    time.sleep(dt)
    return dt


def func_writefile(dt, filepath, string):
    """ Write string in filepath file, then
    sleep dt seconds
    """
    logger = logging.getLogger("func_writefile")
    f = open(filepath, 'w')
    f.write(string)
    f.close()
    logger.info("func_writefile will sleep %f seconds", dt)
    time.sleep(dt)
    return dt
