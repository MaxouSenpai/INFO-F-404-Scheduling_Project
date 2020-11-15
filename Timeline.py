from Event import Event


class Timeline:
    """
    Class that represents a timeline that can contain several events.
    """

    def __init__(self, timeLimit):
        """
        Construct the timeline.
        :param timeLimit: the time limit
        """
        self.timeLimit = timeLimit
        self.cpuState = [Event(Event.Type.IDLE) for _ in range(timeLimit)]
        self.release = [[] for _ in range(timeLimit + 1)]
        self.deadline = [[] for _ in range(timeLimit + 1)]

    def addEvent(self, event, time):
        """
        Add an event at a specified time.
        It adds the event only if the specified
        time is in the range of the timeline.
        :param event: the event
        :param time: the time
        """
        if time < self.timeLimit + 1:
            if event.getType() == Event.Type.RELEASE:
                self.release[time].append(event)
            elif event.getType() == Event.Type.DEADLINE:
                self.deadline[time].append(event)
            elif time < self.timeLimit:
                self.cpuState[time] = event

    def asString(self):
        """
        Return the timeline as a string.
        """
        result = ""
        for t in range(self.timeLimit + 1):
            result += str(t) + " : "
            current = []
            if len(self.release[t]) > 0:
                current.append(" and ".join(e.asString() for e in self.release[t]))

            if len(self.deadline[t]) > 0:
                current.append(" and ".join(e.asString() for e in self.deadline[t]))

            if t < self.timeLimit:
                current.append(self.cpuState[t].asString())

            result += " || ".join(current)
            result += "\n"
        return result
