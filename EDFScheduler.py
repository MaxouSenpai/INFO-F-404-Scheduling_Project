from JobManager import JobManager
from Timeline import Timeline
from Event import Event, EventType


class EDFScheduler:
    """EDFScheduler Object"""

    def __init__(self, timeLimit):
        """
        Construct the EDFScheduler
        :param timeLimit: the time limit
        """
        self.timeLimit = timeLimit

    def schedule(self, partitionedTasks):
        """
        Schedule the specified partitioned tasks
        :param partitionedTasks: the partitioned tasks
        :return: the timelines of the executions of all the cores
        """
        timelines = []
        for i in range(len(partitionedTasks)):
            timelines.append(self.scheduleSingleCore(partitionedTasks[i]))

        return timelines

    def scheduleSingleCore(self, tasks):
        """
        Schedule the specified tasks
        :param tasks: the tasks
        :return: the timeline of the execution
        """
        timeline = Timeline(self.timeLimit+1)
        t = 0
        jobs = [JobManager(j, timeline) for j in tasks]
        currentJob = None

        while t <= self.timeLimit:
            if currentJob is not None and not currentJob.isRunning():
                currentJob = None

            if currentJob is None:  # Search a job to execute
                jobs.sort(key=lambda j: j.getNextDeadLine())
                j = 0

                while j < len(jobs) and currentJob is None:
                    if jobs[j].canRun(t):
                        jobs[j].run()
                        currentJob = jobs[j]
                    j += 1

            if currentJob is None:
                timeline.addEvent(Event(EventType.IDLE), t)

            if t < self.timeLimit:
                for job in jobs:
                    job.addTimeUnit()
            t += 1

        return timeline

    @staticmethod
    def isSchedulable(tasks):
        """
        Verify if the tasks are schedulable
        (if all the tasks can respect their deadline)
        :param tasks: the tasks
        :return: True if schedulable else False
        """
        timeLimit = max(task.getOffset() + task.getDeadline() for task in tasks)  # TODO verify
        t = 0
        jobs = [JobManager(j) for j in tasks]
        currentJob = None

        try:
            while t <= timeLimit:
                if currentJob is not None and not currentJob.isRunning():
                    currentJob = None

                if currentJob is None:  # Search a job to execute
                    jobs.sort(key=lambda j: j.getNextDeadLine())
                    j = 0

                    while j < len(jobs) and currentJob is None:
                        if jobs[j].canRun(t):
                            jobs[j].run()
                            currentJob = jobs[j]
                        j += 1

                for job in jobs:
                    job.addTimeUnit()
                t += 1

        except Exception:
            return False

        return True

    @staticmethod
    def getUtilisationFactor(tasks):
        """
        Return the utilisation factor of the specified tasks
        :param tasks: the tasks
        :return: the utilisation factor
        """
        if len(tasks) == 0:
            return 0
        timeLimit = max(task.getOffset() + task.getDeadline() for task in tasks)  # TODO verify
        t = 0
        jobs = [JobManager(j) for j in tasks]
        currentJob = None
        idleTime = 0

        while t <= timeLimit:
            if currentJob is not None and not currentJob.isRunning():
                currentJob = None

            if currentJob is None:  # Search a job to execute
                jobs.sort(key=lambda j: j.getNextDeadLine())
                j = 0

                while j < len(jobs) and currentJob is None:
                    if jobs[j].canRun(t):
                        jobs[j].run()
                        currentJob = jobs[j]
                    j += 1

            for job in jobs:
                job.addTimeUnit()
            t += 1

        return (timeLimit - idleTime) / timeLimit
