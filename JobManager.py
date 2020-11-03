from Event import Event, EventType


class JobManager:
    """JobManager Object"""

    def __init__(self, task, timeline=None):
        """
        Construct the job manager
        :param task: the task
        :param timeline: the timeline that has to be completed during the execution
        """
        self.task = task
        self.timeline = timeline
        self.executionTime = 0
        self.no = 0  # Number of passed periods
        if self.timeline is not None and self.task.getOffset() == 0:
            self.timeline.addEvent(Event(EventType.RELEASE, [self.task.getID(), self.no]), 0)
        self.t = 0

    def isDeadlineReached(self):
        """Return True if the deadline is reached else False"""
        return self.task.getOffset() + self.no * self.task.getPeriod() + self.task.getDeadline() == self.t

    def isPeriodReached(self):
        """Return True if the period is reached else False"""
        return self.task.getOffset() + (self.no+1) * self.task.getPeriod() == self.t

    def isOffsetReached(self):
        """Return True if the offset is reached"""
        return self.task.getOffset() == self.t

    def addTimeUnit(self):
        """
        Add a unit of time and update the status of the current job
        """
        self.t += 1

        if self.isOffsetReached():
            self.handleRelease()
        else:
            if self.isDeadlineReached():
                self.handleDeadline()

            if self.isPeriodReached():
                self.handlePeriod()

    def getNextDeadLine(self):
        """
        Return the next deadline
        :return: the next deadline
        """
        if self.executionTime == self.task.getWCET():
            return self.task.getOffset() + self.task.getPeriod() * (self.no+1) + self.task.getDeadline()
        else:
            return self.task.getOffset() + self.task.getPeriod() * self.no + self.task.getDeadline()

    def run(self):
        """
        Run the current job
        """
        self.executionTime += 1
        if self.timeline is not None:
            self.timeline.addEvent(Event(EventType.RUNNING, [self.task.getID(), self.no]), self.t)

    def canRun(self):
        """
        Verify if the current job can be run
        :return: True if the current job can run else False
        """
        return self.task.getOffset() <= self.t and self.executionTime < self.task.getWCET()

    def handleRelease(self):
        """Handle the release event"""
        if self.timeline is not None:
            self.timeline.addEvent(Event(EventType.RELEASE, [self.task.getID(), self.no]), self.t)

    def handleDeadline(self):
        """Handle the deadline event"""
        if self.executionTime != self.task.getWCET():
            raise Exception("Deadline not respected")
        if self.timeline is not None:
            self.timeline.addEvent(Event(EventType.DEADLINE, [self.task.getID(), self.no]), self.t)

    def handlePeriod(self):
        """Handle the period event"""
        self.executionTime = 0
        self.no += 1
        if self.timeline is not None:
            self.timeline.addEvent(Event(EventType.RELEASE, [self.task.getID(), self.no]), self.t)
