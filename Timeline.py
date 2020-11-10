from Event import Event


class Timeline:
    """
    Class that represents a timeline containing several events.
    """

    def __init__(self, timeLimit):
        """
        Construct the timeline.
        :param timeLimit: the time limit
        """
        self.events = [[] for _ in range(timeLimit + 1)]
        self.order = {Event.Type.DEADLINE: 0,
                      Event.Type.RELEASE: 1,
                      Event.Type.RUNNING: 2,
                      Event.Type.IDLE: 3}

    def addEvent(self, event, time):
        """
        Add an event at a specified time.
        :param event: the event
        :param time: the time
        """
        self.events[time].append(event)

    def sort(self):
        """
        Sort the timeline.
        If there are multiple events at the time,
        they will be sorted by the order dictionary.
        """
        for e in self.events:
            e.sort(key=lambda s: self.order[s.getType()])

    def asString(self):
        """
        Return the timeline as a string.
        """
        result = ""
        for t in range(len(self.events)):
            result += str(t) + " : "
            result += " and ".join(e.asString() for e in self.events[t])
            result += "\n"
        return result
