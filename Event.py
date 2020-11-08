class Event:
    """Class that represents an event"""

    def __init__(self, eventType, job=None):
        """
        Construct the event
        :param eventType: the type of the event
        :param job: the job (can be omitted, for example an idle event)
        """
        self.eventType = eventType
        self.job = job

    def getType(self):
        """Return the type of the event"""
        return self.eventType

    def getValue(self):
        """Return the value of the event"""
        return self.job

    def asString(self):
        """Return the event as a string"""
        if self.eventType == EventType.IDLE:
            return "Nothing is running"

        elif self.eventType == EventType.RUNNING:
            return self.job.asString() + " is running"

        elif self.eventType == EventType.RELEASE:
            return self.job.asString() + " is released"

        elif self.eventType == EventType.DEADLINE:
            return "Deadline of " + self.job.asString() + " reached"

        else:
            return "Unknown event"


class EventType:
    """Enum all the possible types of events"""
    IDLE = 0
    RUNNING = 1
    RELEASE = 2
    DEADLINE = 3
    toString = {IDLE: "Idle", RUNNING: "Running", RELEASE: "Release", DEADLINE: "Deadline"}
