from Event import Event, EventType


class Job:

    def __init__(self, task, timeline=None):
        self.task = task
        self.running = False
        self.executionTime = 0
        self.idleTime = 0
        self.no = 0  # Number of periods
        self.timeline = timeline
        self.ran = False
        if self.timeline is not None and self.task == 0:
            self.timeline.addEvent(Event(EventType.RELEASE, [self.task.getID(), self.no]), 0)

    def addTimeUnit(self):
        if self.running:
            self.executionTime += 1
        else:
            self.idleTime += 1

        t = self.task.getOffset() + self.no * self.task.getPeriod() + self.executionTime + self.idleTime

        # Finished or still running
        if self.running:
            if self.executionTime == self.task.getWCET():  # Finished
                self.running = False
                self.ran = True

            elif self.timeline is not None:  # Still running
                self.timeline.addEvent(Event(EventType.RUNNING, [self.task.getID(), self.no]), t)

        # Deadline
        if self.executionTime + self.idleTime == self.task.getDeadline():  # Deadline reached
            if self.executionTime != self.task.getWCET():
                raise Exception("Deadline not respected")
            if self.timeline is not None:
                self.timeline.addEvent(Event(EventType.DEADLINE, [self.task.getID(), self.no]), t)

        # Period
        if self.executionTime + self.idleTime == self.task.getPeriod():
            self.executionTime = 0
            self.idleTime = 0
            self.no += 1
            self.ran = False
            if self.timeline is not None:
                self.timeline.addEvent(Event(EventType.RELEASE, [self.task.getID(), self.no]), t)

    def addTimeUnit2(self):
        t = self.task.getOffset() + self.no * self.task.getPeriod() + self.executionTime + self.idleTime
        if self.running:
            self.executionTime += 1
            if self.timeline is not None:
                self.timeline.addEvent(Event(EventType.RUNNING, [self.task.getID(), self.no]), t)
            if self.executionTime == self.task.getWCET():  # Finished
                self.running = False
                self.ran = True

        else:
            self.idleTime += 1

        if self.executionTime + self.idleTime == self.task.getDeadline():
            if self.executionTime != self.task.getWCET():
                raise Exception("Deadline not respected")

            if self.timeline is not None:
                self.timeline.addEvent(Event(EventType.DEADLINE, [self.task.getID(), self.no]), t+1)

        if self.executionTime + self.idleTime == self.task.getPeriod():
            self.executionTime = 0
            self.idleTime = 0
            self.no += 1
            self.ran = False
            if self.timeline is not None:
                self.timeline.addEvent(Event(EventType.RELEASE, [self.task.getID(), self.no]), t+1)

    def getNextDeadLine(self):

        if self.ran:
            return self.task.getOffset() + self.task.getPeriod() * self.no+1 + self.task.getDeadline()
        else:
            return self.task.getOffset() + self.task.getPeriod() * self.no + self.task.getDeadline()

    def run(self):
        self.running = True
        if self.timeline is not None:
            t = self.task.getOffset() + self.no * self.task.getPeriod() + self.idleTime
            self.timeline.addEvent(Event(EventType.RUNNING, [self.task.getID(), self.no]), t)

    def canRun(self, t):
        return self.task.getOffset() <= t and self.executionTime == 0

    def isRunning(self):
        return self.running

    def __repr__(self):
        return "T{}|J{}".format(self.task.getID(), self.no)
