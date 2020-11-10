class Task:
    """
    Class that represents a task.
    """

    def __init__(self, offset, WCET, deadline, period, tid=0):
        """
        Construct the task.
        :param offset: the offset
        :param WCET: the worst case execution time
        :param deadline: the deadline
        :param period: the period
        :param tid: the id (can be omitted)
        """
        self.offset = offset
        self.WCET = WCET
        self.deadline = deadline
        self.period = period
        self.id = tid

    def getOffset(self):
        """
        Return the offset of the task.
        """
        return self.offset

    def getWCET(self):
        """
        Return the worst case execution time of the task.
        """
        return self.WCET

    def getDeadline(self):
        """
        Return the deadline of the task.
        """
        return self.deadline

    def getPeriod(self):
        """
        Return the period of the task.
        """
        return self.period

    def getID(self):
        """
        Return the id of the task.
        """
        return self.id

    def asString(self):
        """
        Return the task as a string without detail.
        """
        return "Task {}".format(self.id)

    def asDetailedString(self):
        """
        Return the task as a string with all the details.
        """
        return "Task {} : offset = {} WCET = {} deadline = {} period = {}".format(self.id, self.offset, self.WCET,
                                                                                  self.deadline, self.period)

    def getUtilisationFactor(self):
        """
        Return the utilisation factor of the task.
        """
        return self.WCET / self.period

    def __repr__(self):
        """
        Return the representation of the task.
        """
        return "Task({},{},{},{},{})".format(self.offset, self.WCET, self.deadline, self.period, self.id)
