# -*- coding: utf-8 -*-
#
#  processcontroller.py
#  
#  Copyright 2017 Vladimir Adamsky <vladimiradamsky@gmail.com>
#  
#  Class ProcessController organizes a job queue 
#  (using multiprocessing.JoinableQueue)
#  and parallel executes tasks from the queue.
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
# 
import logging
from producerprocess import ProducerProcess


class ProcessController:
    """Provide (as wrapper) tasks executing in separate processes"""
    
    def __init__(self, n):
        """Constructor"""
        self.set_max_proc(n)
        self.__pp = ProducerProcess()
    
    def set_max_proc(self, n):
        """Set maximim task processes count"""
        self.__max_proc = n

    def start(self, tasks, max_exec_time):
        """Start tasks execution"""
        logger = logging.getLogger("App:ProcessController")
        # check errors in input data and raise exception
        errmsg = self.__checkerrors(tasks, max_exec_time)
        if errmsg:
            logger.error(errmsg)
            raise NameError(errmsg)
            return -1
        # save tasks count
        self.__tasks_n = len(tasks)
        # calculate optimal maximum task processes count
        self.__max_proc = min(self.__max_proc, len(tasks))
        # set and start ProducerProcess's class process
        self.__pp.set_max_proc(self.__max_proc)
        self.__pp.set_tasks(tasks, max_exec_time)
        self.__pp.start()
    
    def __checkerrors(self, tasks, max_exec_time):
        """Check errors in "start" function input data"""
        if max_exec_time < 1:
            return "max_exec_time is smaller as 1"
        if type(tasks) is not list:
            return "tasks is not list"
        for i in range(len(tasks)):
            task = tasks[i]
            if type(task) is not tuple:
                return "one or several task is not tuple"
            args = task[1]
            if type(args) is not tuple:
                return "args in one or several task is not tuple"
        return None

    def wait(self):
        """Wait all tasks finishing"""
        self.__pp.join()
        return

    def wait_count(self):
        """Get number of tasks that have not started yet""" 
        finished = self.__pp.get_was_finished_count()
        count = self.__tasks_n - finished - self.__max_proc
        return max(0, count)

    def alive_count(self):
        """Get number of running tasks"""
        return self.__pp.get_is_working_count()
