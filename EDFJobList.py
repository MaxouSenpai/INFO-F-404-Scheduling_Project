from Event import Event, EventType


class EDFJobList:
    def __init__(self, timeline=None):
        """Construct the EDFJobList"""
        self.jobsList = []
        self.doneJobsList = []
        self.timeline = timeline
        self.t = -1

    def add(self, job):
        """
        Add the specified job to the active jobs list
        :param job: the job to add
        """
        self.jobsList.append(job)
        self.jobsList.sort(key=lambda j: j.getDeadline())

        if self.timeline is not None:
            self.timeline.addEvent(Event(EventType.RELEASE, [job.getTaskID(), job.getID()]), job.getReleaseTime())

    def addTimeUnit(self):
        """Add a time unit"""
        self.t += 1
        self.update()

        self.updateDoneJobsList()

    def update(self):
        """Update the active jobs list"""
        stop = False
        while len(self.jobsList) > 0 and not stop:
            job = self.jobsList[0]
            if job.isFinished():
                self.remove()
            else:
                if self.jobsList[0].getDeadline() > self.t:
                    self.runJob()
                    stop = True
                else:
                    raise Exception("Deadline not met")

        if self.timeline is not None and len(self.jobsList) == 0:
            self.timeline.addEvent(Event(EventType.IDLE), self.t)

    def updateDoneJobsList(self):
        """Update the done jobs list"""
        i = 0
        stop = False
        while i < len(self.doneJobsList) and not stop:
            job = self.doneJobsList[i]
            if job.getDeadline() <= self.t:
                i += 1
                if self.timeline is not None:
                    self.timeline.addEvent(Event(EventType.DEADLINE, [job.getTaskID(), job.getID()]), self.t)
            else:
                stop = True
        self.doneJobsList = self.doneJobsList[i:]

    def remove(self):
        """Remove the first job of the list and """
        self.doneJobsList.append(self.jobsList[0])
        self.jobsList = self.jobsList[1:]
        self.doneJobsList.sort(key=lambda j: j.getDeadline())

    def verify(self):
        """
        Verify the integrity of the active jobs list
        Verify that the deadline is not passed
        :return:
        """
        for job in self.jobsList:
            if job.getDeadline() < self.t or (job.getDeadline() == self.t and job.executionTime != job.resources):
                return False
        return True

    def runJob(self):
        """Run the first job of the active jobs list"""
        job = self.jobsList[0]
        job.run()
        if self.timeline is not None:
            self.timeline.addEvent(Event(EventType.RUNNING, [job.getTaskID(), job.getID()]), self.t)

    def getAlpha(self, taskID):
        """
        Return the active jobs of the specified task
        :param taskID: the id of the task
        :return: the active jobs of the specified task
        """
        n = 0
        for job in self.jobsList:
            if job.getTaskID() == taskID:
                n += 1
        return n

    def getBeta(self, taskID):
        """
        Return the cumulative CPU time of the oldest active job of
        :param taskID:
        :return:
        """
        for job in self.jobsList:
            if job.getTaskID() == taskID:
                return job.getExecutionTime()
        return 0
