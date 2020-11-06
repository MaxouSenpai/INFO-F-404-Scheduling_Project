from Event import Event, EventType


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
