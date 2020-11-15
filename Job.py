class Job:
    """
    Class that represents a job.
    """

    def __init__(self, releaseTime, deadline, computationRequirement, tid=-1, jid=-1):
        """
        Construct the job.
        :param releaseTime: the release time of the job
        :param deadline: the deadline of the job
        :param computationRequirement: the computation requirement of the job
        :param tid: the id of the task linked to the job (can be omitted)
        :param jid: the id of the job (can be omitted)
        """
        self.releaseTime = releaseTime
        self.deadline = deadline
        self.computationRequirement = computationRequirement
        self.tid = tid
        self.id = jid
        self.executionTime = 0

    def run(self):
        """
        Run the job for an unit of time.
        """
        self.executionTime += 1

    def isFinished(self):
        """
        Return True if the job is finished else False.
        """
        return self.executionTime == self.computationRequirement

    def getDeadline(self):
        """
        Return the deadline.
        """
        return self.deadline

    def getReleaseTime(self):
        """
        Return the release time.
        """
        return self.releaseTime

    def getComputationRequirement(self):
        """
        Return the computation requirement.
        """
        return self.computationRequirement

    def getID(self):
        """
        Return the id of the job.
        """
        return self.id

    def getTaskID(self):
        """
        Return the id of the task linked to the job.
        """
        return self.tid

    def getExecutionTime(self):
        """
        Return the execution time.
        """
        return self.executionTime

    def asString(self):
        """
        Return the job as a string.
        """
        return "T{}-J{}".format(self.getTaskID(), self.getID())

    def __repr__(self):
        """
        Return the representation of the job.
        """
        return "Job({},{},{},{},{},{})".format(self.releaseTime, self.deadline, self.computationRequirement,
                                               self.getTaskID(), self.getID(), self.executionTime)
