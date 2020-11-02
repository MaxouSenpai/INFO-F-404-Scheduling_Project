class Task:

    def __init__(self, offset, WCET, deadline, period, tid=0):
        self.offset = offset
        self.WCET = WCET
        self.deadline = deadline
        self.period = period
        self.id = tid

    def getOffset(self):
        return self.offset

    def getWCET(self):
        return self.WCET

    def getDeadline(self):
        return self.deadline

    def getPeriod(self):
        return self.period

    def getID(self):
        return self.id

    def __repr__(self):
        return str(self.offset) + "|" + str(self.WCET) + "|" + str(self.deadline) + "|" + str(self.period)

    def __str__(self):
        return "Task {} : offset = {} WCET = {} deadline = {} period = {}".format(self.id, self.offset, self.WCET, self.deadline, self.period)
