import time
import logging
from processcontroller import ProcessController
from funcs import func_writefile
# -*- coding: utf-8 -*-
#
#  test.py
#  
#  Copyright 2017 Vladimir Adamsky <vladimiradamsky@gmail.com>
#  
#  This is a test script for ProcessController testing.
#  
#  
LOGGER_FILEPATH = 'logger.log'  # log file path
MAX_TASK_EXECUTE_TIME = 3  # maximum task execution time (seconds)
MAX_TASK_PROCESSES = 2  # maximum task's processes
# dt tuple for calling wait_count() and alive_count()
dt_call_tuple = [0.5, 1, 1, 1, 1, 1, 1, 1]
# dt tuple for tasks
dt_tuple = [1, 2, 2, 4, 1, 2]
# filepath tuple for tasks
fp_tuple = ["file1.txt", "file2.txt", "file3.txt", 
            "file4.txt", "file5.txt", "file6.txt"]
# string tuple for tasks
st_tuple = ["string1", "string2", "string3", 
            "string4", "string5", "string6"]


logging.basicConfig(filename=LOGGER_FILEPATH, 
        level=logging.INFO, 
        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s')


if __name__ == '__main__':
    logger = logging.getLogger("App")
    # create tasks list
    tasks = [(func_writefile, (dt_tuple[i], fp_tuple[i], st_tuple[i])) \
             for i in range(len(dt_tuple))]
    # create and start ProcessController process
    pc = ProcessController(MAX_TASK_PROCESSES)
    pc.start(tasks, MAX_TASK_EXECUTE_TIME)
    # testing
    for dt in dt_call_tuple:
        time.sleep(dt)
        logger.info("wait_count(): %d", pc.wait_count())
        logger.info("alive_count(): %d", pc.alive_count())
    # wait for all tasks finishing
    pc.wait()
    print("end program")