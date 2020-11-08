from Event import Event, EventType


class EDFJobsList:
    """
    Class that represents the list of jobs of an edf scheduler.
    The particularity is that the activeJobsList and the doneJobsList
    are always sorted by the deadlines of their jobs.
    """
    def __init__(self, timeline=None):
        """
        Construct the EDFJobList
        :param timeline: the timeline to be completed as an event occurs (can be omitted)
        """
        self.activeJobsList = []  # always sorted by deadline (ascending)
        self.doneJobsList = []  # always sorted by deadline (ascending)
        self.timeline = timeline
        self.t = -1

    def add(self, job):
        """
        Add the specified job to the active jobs list
        :param job: the job to add
        """
        self.activeJobsList.append(job)
        self.activeJobsList.sort(key=lambda j: j.getDeadline())

        if self.timeline is not None:
            self.timeline.addEvent(Event(EventType.RELEASE, job), job.getReleaseTime())

    def addTimeUnit(self):
        """Add a time unit and update the whole object"""
        self.t += 1
        self.updateActiveJobsList()
        self.updateDoneJobsList()

    def updateActiveJobsList(self):
        """
        Update the active jobs list.
        Put all the first jobs that are finished in the doneJobsList
        and run the first unfinished job.
        """
        stop = False
        while len(self.activeJobsList) > 0 and not stop:
            job = self.activeJobsList[0]
            if job.isFinished():
                self.removeFromActive()
            else:
                if self.activeJobsList[0].getDeadline() > self.t:
                    self.runJob()
                    stop = True
                else:
                    raise Exception("Deadline not met")

        if self.timeline is not None and len(self.activeJobsList) == 0:
            self.timeline.addEvent(Event(EventType.IDLE), self.t)

    def updateDoneJobsList(self):
        """
        Update the done jobs list.
        Remove the jobs of the doneJobsList if their deadlines are reached.
        """
        i = 0
        stop = False
        while i < len(self.doneJobsList) and not stop:
            job = self.doneJobsList[i]
            if job.getDeadline() <= self.t:
                i += 1
                if self.timeline is not None:
                    self.timeline.addEvent(Event(EventType.DEADLINE, job), self.t)
            else:
                stop = True
        self.doneJobsList = self.doneJobsList[i:]

    def removeFromActive(self):
        """Remove the first job of the active activeJobsList and add it to the doneJobsList"""
        self.doneJobsList.append(self.activeJobsList[0])
        self.activeJobsList = self.activeJobsList[1:]
        self.doneJobsList.sort(key=lambda j: j.getDeadline())

    def verify(self):
        """
        Verify the integrity of the active jobs list.
        Verify that the deadlines are not passed.
        """
        for job in self.activeJobsList:
            if job.getDeadline() < self.t or \
                    (job.getDeadline() == self.t and job.getExecutionTime() != job.getComputationRequirement()):
                return False
        return True

    def runJob(self):
        """Run the first job of the active jobs list"""
        job = self.activeJobsList[0]
        job.run()
        if self.timeline is not None:
            self.timeline.addEvent(Event(EventType.RUNNING, job), self.t)

    def getAlpha(self, taskID):
        """
        Return the active jobs of the specified task
        :param taskID: the id of the task
        :return: the active jobs of the specified task
        """
        n = 0
        for job in self.activeJobsList:
            if job.getTaskID() == taskID:
                n += 1
        return n

    def getBeta(self, taskID):
        """
        Return the cumulative CPU time of the oldest active job of the specified task
        :param taskID: the id of the task
        :return: the cumulative CPU time of the oldest active job of the specified task
        """
        for job in self.activeJobsList:
            if job.getTaskID() == taskID:
                return job.getExecutionTime()
        return 0
