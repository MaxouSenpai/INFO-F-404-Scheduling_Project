from Event import EventType


class Timeline:
    """Class that represents a timeline containing several events [t)"""

    def __init__(self, timeLimit):
        """
        Construct the Timeline
        :param timeLimit: the time limit
        """
        self.events = [[] for _ in range(timeLimit)]
        self.order = {EventType.DEADLINE: 0,
                      EventType.RELEASE: 1,
                      EventType.RUNNING: 2,
                      EventType.IDLE: 3}

    def addEvent(self, event, time):
        """
        Add an event at a specified time
        :param event: the event
        :param time: the time
        """
        self.events[time].append(event)

    def sort(self):
        """
        Sort the timeline
        If there are multiple events at the time,
        they will be sorted by the order dictionary
        """
        for e in self.events:
            e.sort(key=lambda s: self.order[s.getType()])

    def asString(self):
        """Return the timeline as a string"""
        result = ""
        for t in range(len(self.events)):
            result += str(t) + " : "
            result += " and ".join(e.asString() for e in self.events[t])
            result += "\n"
        return result
