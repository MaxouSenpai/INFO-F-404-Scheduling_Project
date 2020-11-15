import math

from Event import Event
from Job import Job
from Timeline import Timeline


class EDFScheduler:
    """
    Class that represents the fixed job priority scheduler EDF (earliest deadline first).
    """
    def __init__(self):
        """
        Construct the EDF scheduler.
        """
        self.activeJobs = []
        self.timeline = None
        self.tasks = []
        self.t = 0
        self.nbReleasedJob = None

    def reset(self):
        """
        Reset the EDF scheduler.
        """
        self.activeJobs = []
        self.timeline = None
        self.tasks = None
        self.t = 0
        self.nbReleasedJob = None

    def scheduleAll(self, partitionedTasks, timeLimit):
        """
        Schedule the specified partitioned tasks.
        :param partitionedTasks: the partitioned tasks
        :param timeLimit: the time limit
        :return: the list of all the timelines
        """
        timelines = []
        for tasks in partitionedTasks:
            timelines.append(self.schedule(tasks, timeLimit))

        return timelines

    def schedule(self, tasks, timeLimit):
        """
        Schedule the specified tasks and fill the timeline [0,timeLimit].
        :param tasks: the list of tasks
        :param timeLimit: the time limit
        :return: the timeline
        """
        self.reset()
        self.tasks = tasks
        self.nbReleasedJob = [0 for _ in range(len(tasks))]
        self.timeline = Timeline(timeLimit)

        while self.t < timeLimit:
            # at this point t)
            self.findJobsToRelease()
            self.findFinishedJobs()
            self.verifyDeadlines()
            # at this point t]
            self.findJobToRun()
            # at this point t+1)
            self.t += 1

        self.findJobsToRelease()
        self.findFinishedJobs()
        self.verifyDeadlines()
        return self.timeline

    def isSchedulable(self, tasks):
        """
        Verify if the specified tasks are schedulable.
        :param tasks: the tasks
        :return: True if schedulable else False
        """
        try:
            self.reset()
            self.tasks = tasks
            self.nbReleasedJob = [0 for _ in range(len(tasks))]

            P = math.lcm(*[task.getPeriod() for task in tasks])  # Hyper-Period
            timeLimit = max(task.getOffset() for task in tasks) + 2 * P

            c1, c2 = None, None

            while self.t < timeLimit:
                # at this point t)
                self.findJobsToRelease()
                self.findFinishedJobs()
                self.verifyDeadlines()
                # at this point t]
                if self.t == max(task.getOffset() for task in tasks) + P:
                    c1 = self.getConfiguration()
                #
                self.findJobToRun()
                # at this point t+1)
                self.t += 1

            # at this point timeLimit)
            self.findJobsToRelease()
            self.findFinishedJobs()
            self.verifyDeadlines()
            # at this point timeLimit]
            c2 = self.getConfiguration()

            return c1 == c2

        except Exception:
            return False

    def releaseJob(self, job):
        """
        Release the specified job.
        Add the job to the activeJobs list.
        :param job: the job to release
        """
        self.activeJobs.append(job)
        if self.timeline is not None:
            self.timeline.addEvent(Event(Event.Type.RELEASE, job), self.t)
            self.timeline.addEvent(Event(Event.Type.DEADLINE, job), job.getDeadline())

    def findJobsToRelease(self):
        """
        Release all the jobs that need to be.
        """
        for i in range(len(self.tasks)):
            task = self.tasks[i]
            k = self.nbReleasedJob[i]
            if task.getOffset() + k * task.getPeriod() == self.t:
                self.releaseJob(Job(self.t, self.t + task.getDeadline(), task.getWCET(), task.getID(), k))
                self.nbReleasedJob[i] += 1

    def findFinishedJobs(self):
        """
        Remove all the finished jobs.
        """
        i = 0
        while i < len(self.activeJobs):
            job = self.activeJobs[i]
            if job.isFinished():
                self.activeJobs.remove(job)
            else:
                i += 1

    def findJobToRun(self):
        """
        Run the job that has the earliest deadline.
        """
        self.activeJobs.sort(key=lambda j: j.getDeadline())
        if len(self.activeJobs) > 0:
            job = self.activeJobs[0]
            job.run()
            if self.timeline is not None:
                self.timeline.addEvent(Event(Event.Type.RUNNING, job), self.t)

    def verifyDeadlines(self):
        """
        Raise an exception if a deadline is not met.
        """
        for job in self.activeJobs:
            if job.getDeadline() <= self.t and not job.isFinished():
                raise Exception("Deadline of " + job.asString() + " not met")

    def getConfiguration(self):
        """
        Return the current configuration.
        """
        res = [[0, 0, 0]for _ in range(len(self.tasks))]
        for i in range(len(self.tasks)):
            task = self.tasks[i]
            y = self.getGamma(task)
            a = self.getAlpha(task.getID())
            b = self.getBeta(task.getID())
            res[i] = [y, a, b]

        return res

    def getGamma(self, task):
        """
        The time elapsed since the last request.
        :param task: the task
        :return: The time elapsed since the last request
        """
        if self.t >= task.getOffset():
            return (self.t - task.getOffset()) % task.getPeriod()

        else:
            return self.t - task.getOffset()

    def getAlpha(self, taskID):
        """
        Return the number of active jobs of the specified task.
        :param taskID: the id of the task
        :return: the number of active jobs of the specified task
        """
        n = 0
        for job in self.activeJobs:
            if job.getTaskID() == taskID:
                n += 1
        return n

    def getBeta(self, taskID):
        """
        Return the cumulative CPU time of the oldest active job of the specified task.
        :param taskID: the id of the task
        :return: the cumulative CPU time of the oldest active job of the specified task
        """
        self.activeJobs.sort(key=lambda j: j.getReleaseTime())
        for job in self.activeJobs:
            if job.getTaskID() == taskID:
                return job.getExecutionTime()
        return 0
