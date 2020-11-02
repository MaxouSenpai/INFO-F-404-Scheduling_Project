from Event import Event, EventType


class JobManager:  # TODO fix remaining offset bugs
    """JobManager Object"""

    def __init__(self, task, timeline=None):
        """
        Construct the job manager
        :param task: the task
        :param timeline: the timeline that has to be completed during the execution
        """
        self.task = task
        self.running = False
        self.executionTime = 0
        self.idleTime = 0
        self.no = 0  # Number of passed periods
        self.timeline = timeline
        self.ran = False
        if self.timeline is not None and self.task == 0:
            self.timeline.addEvent(Event(EventType.RELEASE, [self.task.getID(), self.no]), 0)
        self.t = 0

    def addTimeUnit(self):
        """
        Add a unit of time and update the status of the current job
        """
        self.t += 1
        if self.running:
            self.executionTime += 1
        else:
            self.idleTime += 1

        # Finished or still running
        if self.running:
            if self.executionTime == self.task.getWCET():  # Finished
                self.running = False
                self.ran = True

            elif self.timeline is not None:  # Still running
                self.timeline.addEvent(Event(EventType.RUNNING, [self.task.getID(), self.no]), self.t)

        # Deadline
        if self.executionTime + self.idleTime == self.task.getDeadline():  # Deadline reached
            if self.executionTime != self.task.getWCET():
                raise Exception("Deadline not respected")
            if self.timeline is not None:
                self.timeline.addEvent(Event(EventType.DEADLINE, [self.task.getID(), self.no]), self.t)

        # Period
        if self.executionTime + self.idleTime == self.task.getPeriod() or self.task.getOffset() == self.t:
            self.executionTime = 0
            self.idleTime = 0
            self.no += 1
            self.ran = False
            if self.timeline is not None:
                self.timeline.addEvent(Event(EventType.RELEASE, [self.task.getID(), self.no]), self.t)

    def getNextDeadLine(self):
        """
        Return the next deadline
        :return: the next deadline
        """
        if self.ran:
            return self.task.getOffset() + self.task.getPeriod() * self.no+1 + self.task.getDeadline()
        else:
            return self.task.getOffset() + self.task.getPeriod() * self.no + self.task.getDeadline()

    def run(self):
        """
        Run the current job
        """
        self.running = True
        if self.timeline is not None:
            t = self.task.getOffset() + self.no * self.task.getPeriod() + self.idleTime
            self.timeline.addEvent(Event(EventType.RUNNING, [self.task.getID(), self.no]), t)

    def canRun(self):
        """
        Verify if the current job can be run
        :return: True if the current job can run else False
        """
        return self.task.getOffset() <= self.t and self.executionTime == 0

    def isRunning(self):
        """
        Verify if the current job is running
        :return: True if the current job is running else False
        """
        return self.running
