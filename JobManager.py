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

    def addTimeUnit(self):
        """
        Add a unit of time and update the status of the current job
        """
        self.t += 1

        self.checkDeadline()
        self.checkPeriod()

    def checkDeadline(self):
        """
        Check if the deadline is reached and act accordingly
        """
        if self.task.getOffset() + self.no * self.task.getPeriod() + self.task.getDeadline() == self.t:
            if self.executionTime != self.task.getWCET():
                raise Exception("Deadline not respected")
            if self.timeline is not None:
                self.timeline.addEvent(Event(EventType.DEADLINE, [self.task.getID(), self.no]), self.t)

    def checkPeriod(self):
        """
        Check if the period is reached and act accordingly
        """
        if self.task.getOffset() + (self.no+1) * self.task.getPeriod() == self.t:
            self.executionTime = 0
            self.no += 1
            if self.timeline is not None:
                self.timeline.addEvent(Event(EventType.RELEASE, [self.task.getID(), self.no]), self.t)

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
