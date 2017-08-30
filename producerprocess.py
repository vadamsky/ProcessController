# -*- coding: utf-8 -*-
#
#  producerprocess.py
#  
#  Copyright 2017 Vladimir Adamsky <vladimiradamsky@gmail.com>
#  
#  Class ProducerProcess provides process control and tasks running.
#  
#  
import time
import logging
from multiprocessing import Process, Array, JoinableQueue
from funcs import func, func_writefile


class ProducerProcess(Process):
    """Generates processes for executing tasks"""
    
    def __init__(self):
        """Constructor"""
        Process.__init__(self)
        self.__q = JoinableQueue()
    
    def set_tasks(self, tasks, max_exec_time):
        """Set tasks list and any task maximum execute time"""
        self.__tasks = tasks
        self.__max_exec_time = max_exec_time

    def set_max_proc(self, max_proc):
        """Set maximum task processes count"""
        self.__max_proc = max_proc
        # Create and fill shared arrays
        self.__tasks_was_finished = Array('i', range(max_proc))
        self.__is_working = Array('b', range(max_proc))
        for index in range(max_proc):
            self.__tasks_was_finished[index] = 0
            self.__is_working[index] = False

    def get_is_working_count(self):
        """Get working tasks count"""
        return sum(self.__is_working)
    
    def get_was_finished_count(self):
        """Get finished tasks count"""
        return sum(self.__tasks_was_finished)
    
    def __create_consumers(self):
        """Create consumers processes"""
        for index in range(0, self.__max_proc):
            cons_p = Process(target=self.consumer, 
                             args=(self.__q, index,
                                   self.__tasks_was_finished,
                                   self.__is_working))
            cons_p.daemon = False
            cons_p.start()

    def __close_queue(self):
        """Put signal marks in queue and close it"""
        for i in range(0, self.__max_proc):
            self.__q.put(None)
        self.__q.close()

    def consumer(self, input_q, index, tasks_was_finished, is_working):
        """Consumer's process function creates worker process
        (for executing task) and terminates it if time is over
        """
        logger = logging.getLogger("App.ProducerProcess")
        is_working[index] = True
        while True:
            item = input_q.get()
            if item is None:  # signal mark: need exit
                break
            # Execute task in worker process
            wrk_p = Process(target=self.worker, args=(item,))
            wrk_p.daemon = True
            wrk_p.start()
            # join or terminate worker process
            wrk_p.join(timeout=self.__max_exec_time)
            if wrk_p.is_alive():
                logger.info("Terminate worker")
                wrk_p.terminate()
            # report about task finishing
            tasks_was_finished[index] += 1
            input_q.task_done()
        # preparation for exit
        is_working[index] = False
        input_q.task_done()

    def worker(self, item):
        """Worker's process function execute task"""
        logger = logging.getLogger("App.ProducerProcess")
        startTime = time.time()
        # extract and start task function
        f = item[0]
        args = item[1]
        f(*args)
        logger.info("Worker ends it's work by %f seconds.", 
                    time.time() - startTime)

    def run(self):
        """ProducerProcess's process function puts task items in queue
        and wait for joining the queue
        """
        self.__create_consumers() # create consumer's processes
        # put task items in queue
        for task in self.__tasks:
            self.__q.put(task)
        # put signal marks in queue and close it
        self.__close_queue()
        # join queue
        self.__q.join()
