import numpy as np

from EDFJobsList import EDFJobsList
from JobManager import JobManager
from Timeline import Timeline


class Scheduler:
    """Class that represents a fixed job priority scheduler"""
    def __init__(self, timeLimit, schedulerType):
        """
        Construct the scheduler
        :param timeLimit: the time limit
        """
        self.timeLimit = timeLimit
        self.type = schedulerType

    def schedule(self, partitionedTasks):
        """
        Schedule the specified partitioned tasks
        :param partitionedTasks: the partitioned tasks
        :return: the list of the timelines of the executions of all the processor
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
        :return: the timeline of the execution [0,t]
        """
        timeline = Timeline(self.timeLimit + 1)
        t = 0
        jobsList = EDFJobsList(timeline)
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
        jobsList = EDFJobsList()
        jobManagers = [JobManager(j, jobsList) for j in tasks]
        c1, c2 = None, None

        while t < timeLimit:
            if t == max(task.getOffset() for task in tasks) + P:
                c1 = Scheduler.getConfiguration(t, tasks, jobsList)

            for jobManager in jobManagers:
                jobManager.addTimeUnit()

            jobsList.addTimeUnit()

            t += 1

        c2 = Scheduler.getConfiguration(t, tasks, jobsList)

        return jobsList.verify() and c1 == c2

    @staticmethod
    def getConfiguration(t, tasks, jobsList):
        """Return the current configuration"""
        res = []
        for task in tasks:
            if t >= task.getOffset():
                y = (t - task.getOffset()) % task.getPeriod()

            else:
                y = (t - task.getOffset())

            a = jobsList.getAlpha(task.getID())
            b = jobsList.getBeta(task.getID())
            res.append([y, a, b])

        return res
