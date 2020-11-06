from JobManager import JobManager
from Timeline import Timeline
from Event import Event, EventType
import numpy as np


class EDFScheduler:
    """EDFScheduler Object"""

    def __init__(self, timeLimit):
        """
        Construct the EDFScheduler
        :param timeLimit: the time limit
        """
        self.timeLimit = timeLimit

    def schedule(self, partitionedTasks):
        """
        Schedule the specified partitioned tasks
        :param partitionedTasks: the partitioned tasks
        :return: the timelines of the executions of all the cores
        """
        timelines = []
        for i in range(len(partitionedTasks)):
            timelines.append(self.scheduleSingleCore(partitionedTasks[i]))

        return timelines

    def scheduleSingleCore(self, tasks):
        """
        Schedule the specified tasks
        :param tasks: the tasks
        :return: the timeline of the execution
        """
        timeline = Timeline(self.timeLimit+1)
        t = 0
        jobList = EDFJobList(timeline)
        jobManagers = [JobManager(j, jobList) for j in tasks]

        while t <= self.timeLimit:  # TODO verify time limit
            for jobManager in jobManagers:
                jobManager.addTimeUnit()

            if t < self.timeLimit:
                jobList.addTimeUnit()
            t += 1

        return timeline

    @staticmethod
    def isSchedulable(tasks):
        """
        Verify if the tasks are schedulable
        (if all the tasks can respect their deadline)
        :param tasks: the tasks
        :return: True if schedulable else False
        """
        P = np.lcm.reduce([task.getPeriod() for task in tasks])  # Hyper-Period
        timeLimit = max(task.getOffset() for task in tasks) + 2 * P  # TODO verify
        t = 0
        jobList = EDFJobList()
        jobManagers = [JobManager(j, jobList) for j in tasks]

        while t <= timeLimit:  # TODO verify time limit
            for jobManager in jobManagers:
                jobManager.addTimeUnit()

            if t < timeLimit:
                jobList.addTimeUnit()
            t += 1

        return jobList.verify()  # TODO P96


class EDFJobList:
    def __init__(self, timeline=None):
        self.jobList = []
        self.doneJobList = []
        self.timeline = timeline
        self.t = -1

    def add(self, job):
        self.jobList.append(job)
        self.jobList.sort(key=lambda j: j.getDeadline())

        if self.timeline is not None:
            self.timeline.addEvent(Event(EventType.RELEASE, [job.getTaskID(), job.getID()]), job.getReleaseTime())

    def addTimeUnit(self):
        self.t += 1
        if len(self.jobList) >= 1:
            if not self.jobList[0].isFinished():
                self.runJob()
            else:
                self.remove()
                if len(self.jobList) >= 1:
                    self.runJob()
                elif self.timeline is not None:
                    self.timeline.addEvent(Event(EventType.IDLE), self.t)
        elif self.timeline is not None:
            self.timeline.addEvent(Event(EventType.IDLE), self.t)

        i = 0
        stop = False
        while i < len(self.doneJobList) and not stop:
            job = self.doneJobList[i]
            if job.getDeadline() <= self.t:
                i += 1
                if self.timeline is not None:
                    self.timeline.addEvent(Event(EventType.DEADLINE, [job.getTaskID(), job.getID()]), self.t)
            else:
                stop = True

        self.doneJobList = self.doneJobList[i:]

    def remove(self):
        self.doneJobList.append(self.jobList[0])
        self.jobList = self.jobList[1:]
        self.doneJobList.sort(key=lambda j: j.getDeadline())

    def verify(self):
        for job in self.jobList:
            if job.getDeadline() < self.t or (job.getDeadline() == self.t and job.executionTime != job.resources):
                return False
        return True

    def runJob(self):
        job = self.jobList[0]
        job.run()
        if self.timeline is not None:
            self.timeline.addEvent(Event(EventType.RUNNING, [job.getTaskID(), job.getID()]), self.t)
