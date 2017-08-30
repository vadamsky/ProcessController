# ProcessController
ProcessController organizes a job queue (using multiprocessing.JoinableQueue) and parallel executes tasks from the queue.

## Methods
- set_max_proc(n) - sets the maximum number of simultaneous jobs.
+ start(tasks, max_exec_time) - queues all tasks from tasks list. In the event that the maximum number of 
  concurrent jobs is not reached, the method starts execution of jobs from the queue until this limit is reached. 
  Running a task represents the creation of a new process, which executes the corresponding function with its arguments. 
  In this case, each running process for tasks from tasks should not work longer than max_exec_time.
  + tasks - the list of tasks. The job represents a tuple of the form: 
    (function, tuple of input arguments for a function).
    Example: 
    ```
    tasks = [(function0, (f0_arg0, f0_arg1)), 
             (function1, (f1_arg0, f1_arg1, f1_arg2)), 
             (function2, (f2_arg0,))]
    ```               
  + max_exec_time - the maximum time (in seconds) for each task from the tasks list.
- wait() - wait until all the jobs in the queue have completed their execution.
- wait_count() - returns the number of jobs that are left to run.
- alive_count() - returns the number of jobs currently executing.

## Notes
* The number of processes for direct execution of tasks is calculated by the formula N = min(n, len(tasks)), 
  where n is argument of set_max_proc function, and tasks - tasks list.
* In addition to N processes, N + 1 processes are also started for management.
