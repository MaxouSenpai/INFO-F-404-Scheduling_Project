import numpy as np

from EDFJobList import EDFJobList
from JobManager import JobManager
from Timeline import Timeline


class Scheduler:
    """Scheduler Object"""
    def __init__(self, timeLimit, schedulerType):
        """
        Construct the Scheduler
        :param timeLimit: the time limit
        """
        self.timeLimit = timeLimit
        self.type = schedulerType

    def schedule(self, partitionedTasks):
        """
        Schedule the specified partitioned tasks
        :param partitionedTasks: the partitioned tasks
        :return: the timelines of the executions of all the cores
        """
        return [self.scheduleUniprocessor(tasks) for tasks in partitionedTasks]

    def scheduleUniprocessor(self, tasks):
        """
        Schedule the specified tasks
        :param tasks: the tasks
        :return: the timeline of the execution
        """
        if self.type == "EDF":
            return self.EDFSchedule(tasks)
        else:
            raise Exception("Unknown scheduler option")

    def EDFSchedule(self, tasks):
        """
        Schedule the specified tasks with the earliest deadline first method
        :param tasks: the tasks
        :return: the timeline of the execution
        """
        timeline = Timeline(self.timeLimit + 1)
        t = 0
        jobsList = EDFJobList(timeline)
        jobManagers = [JobManager(j, jobsList) for j in tasks]

        while t <= self.timeLimit:
            for jobManager in jobManagers:
                jobManager.addTimeUnit()

            if t < self.timeLimit:
                jobsList.addTimeUnit()
            t += 1

        return timeline

    @staticmethod
    def isSchedulable(tasks):
        """
        Verify if the tasks are schedulable
        (if all the tasks can respect their deadline)
        EDF scheduler can schedule everything that is schedulable
        :param tasks: the tasks
        :return: True if schedulable else False
        """
        P = np.lcm.reduce([task.getPeriod() for task in tasks])  # Hyper-Period
        timeLimit = max(task.getOffset() for task in tasks) + 2 * P
        t = 0
        jobsList = EDFJobList()
        jobManagers = [JobManager(j, jobsList) for j in tasks]

        while t <= timeLimit:
            for jobManager in jobManagers:
                jobManager.addTimeUnit()

            if t < timeLimit:
                jobsList.addTimeUnit()
            t += 1

        return jobsList.verify()  # TODO P96
