class Event:
    """Event Object"""

    def __init__(self, eventType, value=None):
        self.eventType = eventType
        self.value = value

    def getType(self):
        """Return the type of the event"""
        return self.eventType

    def getValue(self):
        """Return the value of the event"""
        return self.value

    def __repr__(self):
        result = EventType.conversion[self.eventType]
        if self.value is not None:
            result += " : T" + str(self.value[0]) + " J" + str(self.value[1])
        return result

    def __str__(self):
        if self.eventType == EventType.IDLE:
            return "Nothing is running"

        elif self.eventType == EventType.RUNNING:
            return "T" + str(self.value[0]) + "-J" + str(self.value[1]) + " is running"

        elif self.eventType == EventType.RELEASE:
            return "T" + str(self.value[0]) + "-J" + str(self.value[1]) + " is released"

        elif self.eventType == EventType.DEADLINE:
            return "Deadline of T" + str(self.value[0]) + "-J" + str(self.value[1]) + " reached"

        else:
            return "unknown"


class EventType:
    """Enum all the possible types of events"""
    IDLE = 0
    RUNNING = 1
    RELEASE = 2
    DEADLINE = 3
    conversion = {IDLE: "Idle", RUNNING: "Running", RELEASE: "Release", DEADLINE: "Deadline"}
