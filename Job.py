class Job:
    """Job Object"""

    def __init__(self, releaseTime, deadline, resources, tid=-1, jid=-1):
        self.releaseTime = releaseTime
        self.deadline = deadline
        self.resources = resources
        self.tid = tid
        self.id = jid
        self.executionTime = 0

    def run(self):
        self.executionTime += 1

    def canRun(self):
        return self.executionTime < self.resources

    def isFinished(self):
        return self.executionTime == self.resources

    def isDeadlineReached(self, t):
        return self.deadline == t

    def getDeadline(self):
        return self.deadline

    def getReleaseTime(self):
        return self.releaseTime

    def getID(self):
        return self.id

    def getTaskID(self):
        return self.tid

    def __repr__(self):
        return "T{}J{}".format(self.getTaskID(), self.getID())
