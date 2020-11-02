from Event import EventType


class Timeline:
    """
    Timeline Object
    [t)
    """
    order = {EventType.RUNNING: 0,
             EventType.IDLE: 1,
             EventType.DEADLINE: 2,
             EventType.RELEASE: 3}

    def __init__(self, timeLimit):
        """
        Construct the Timeline
        :param timeLimit: the time limit
        """
        self.events = [[] for _ in range(timeLimit)]

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
        they will be sorted by the order dictionary of the Timeline class
        """
        for e in self.events:
            e.sort(key=lambda s: Timeline.order[s.getType()])

    def __str__(self):
        result = ""
        for t in range(len(self.events)):
            result += str(t) + " : "
            result += " and ".join(str(e) for e in self.events[t])
            result += "\n"
        return result
