from Job import Job


class JobManager:
    """JobManager Object"""
    def __init__(self, task, jobList):
        self.task = task
        self.jobList = jobList

        self.t = -1
        self.nbReleasedJobs = 0

    def addTimeUnit(self):
        self.t += 1

        if self.isOffsetReached() or (self.isOffsetPassed() and self.isPeriodReached()):
            self.addJob()

    def isPeriodReached(self):
        """Return True if the period is reached else False"""
        return self.task.getOffset() + self.nbReleasedJobs * self.task.getPeriod() == self.t

    def isOffsetReached(self):
        """Return True if the offset is reached else False"""
        return self.task.getOffset() == self.t

    def isOffsetPassed(self):
        """Return True if the offset is passed else False"""
        return self.task.getOffset() < self.t

    def addJob(self):
        """Add a job to the list"""
        tempJob = Job(self.t, self.t + self.task.getDeadline(), self.task.getWCET(), self.task.getID(),
                      self.nbReleasedJobs)
        self.jobList.add(tempJob)
        self.nbReleasedJobs += 1
