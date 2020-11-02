from Event import EventType


class Timeline:
    """
    [t)
    """
    order = {EventType.RUNNING: 0,
             EventType.IDLE: 0,
             EventType.DEADLINE: 1,
             EventType.RELEASE: 2}

    def __init__(self, timeLimit):
        self.events = [[] for _ in range(timeLimit)]

    def addEvent(self, event, time):
        self.events[time].append(event)

    def addPeriodicEvent(self, event, offset, deadline, period):
        pass

    def sort(self):
        for e in self.events:
            e.sort(key=lambda s: Timeline.order[s.getType()])

    def __str__(self):
        result = ""
        for t in range(len(self.events)):
            result += str(t) + " : "
            result += " and ".join(str(e) for e in self.events[t])
            result += "\n"
        return result
