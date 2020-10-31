"""
INFO-F-404
Maxime Hauwaert
461714

Notes:
    WCET: Worst Case Execution Time
    offset: release
"""
import sys


class Task:
    def __init__(self, offset, WCET, deadline, period, id):
        self.offset = offset
        self.WCET = WCET
        self.deadline = deadline
        self.period = period
        self.id = id

    def getOffset(self):
        return self.offset

    def getWCET(self):
        return self.WCET

    def getDeadline(self):
        return self.deadline

    def getPeriod(self):
        return self.period

    def __repr__(self):
        return str(self.offset) + "|" + str(self.WCET) + "|" + str(self.deadline) + "|" + str(self.period)

    def __lt__(self, other):
        return self.deadline < other.getDeadline()


class Partitioner:
    def __init__(self, heuristic, sort, cores):
        self.heuristic = heuristic
        self.sort = sort
        self.cores = cores

    def partition(self, tasks):
        print(self.heuristic, self.sort, self.cores)

        if self.heuristic == "ff":
            partitionedTasks = self.firstFit(tasks)
        elif self.heuristic == "wf":
            partitionedTasks = self.worstFit(tasks)
        elif self.heuristic == "bf":
            partitionedTasks = self.bestFit(tasks)
        else:
            partitionedTasks = self.nextFit(tasks)

        if self.sort == "iu":
            partitionedTasks = self.increaseUtilisation(partitionedTasks)
        else:
            partitionedTasks = self.decreasingUtilisation(partitionedTasks)

        return [partitionedTasks]

    def firstFit(self, tasks):
        return tasks

    def worstFit(self, tasks):
        return tasks

    def bestFit(self, tasks):
        return tasks

    def nextFit(self, tasks):
        return tasks

    def increaseUtilisation(self, partitionedTasks):
        return partitionedTasks

    def decreasingUtilisation(self, partitionedTasks):
        return partitionedTasks


class EDFScheduler:
    def __init__(self, timeLimit):
        self.timeLimit = timeLimit

    def schedule(self, partitionedTasks):
        print(self.timeLimit)
        print(partitionedTasks)

        for i in range(len(partitionedTasks)):
            self.scheduleSingleCore(partitionedTasks[i], i)

        print(partitionedTasks)

    def scheduleSingleCore(self, tasks, no):
        t = 0
        jobs = [Job(j) for j in tasks]
        jobs.sort()  # earliest deadline first
        events = []
        currentJob = None
        while t < self.timeLimit:

            for job in jobs:
                if job.isReleased(t):
                    events.append([t, "rel", "J" + str(job.task.id)])
            # deadline
            if currentJob is None or not currentJob.canStillRun():
                currentJob = None
                for job in jobs:
                    if job.canRerun() or job.canRun(t):
                        currentJob = job
                        currentJob.run()
                        break

            if currentJob is not None:
                events.append([t, "run", "T" + str(currentJob.task.id) + "|J" + str(currentJob.id)])
            else:
                events.append([t, "idle"])

            for job in jobs:
                job.addTimeUnit()

            t += 1
        print(events)


class Job:
    def __init__(self, task):
        self.task = task
        self.executionTime = 0
        self.idleTime = 0
        self.id = -1
        self.running = False

    def isReleased(self, t):
        return self.task.getOffset() == t

    def addTimeUnit(self):
        if self.running:
            self.executionTime += 1
            if self.executionTime == self.task.getWCET():
                self.running = False
        else:
            self.idleTime += 1

    def isRunning(self):
        return self.running

    def canStillRun(self):
        return self.executionTime < self.task.getWCET()

    def canRerun(self):
        return self.executionTime + self.idleTime >= self.task.getPeriod()

    def canRun(self, t):
        return t >= self.task.getOffset() and self.executionTime == 0

    def run(self):
        self.id += 1
        self.idleTime = 0
        self.executionTime = 0
        self.running = True

    def __lt__(self, other):
        return self.task < other.task

def taskParser(taskFile):
    tasks = []
    with open(taskFile) as file:
        id = 0
        for line in file:
            attr = line.split(" ")
            if len(attr) == 4:
                tasks.append(Task(int(attr[0]), int(attr[1]), int(attr[2]), int(attr[3]), id))
            id += 1
    return tasks


def run(taskSetFile, heuristic, sort, limit, cores):
    partitioner = Partitioner(heuristic, sort, cores)
    tasks = taskParser(taskSetFile)
    partitionedTask = partitioner.partition(tasks)

    scheduler = EDFScheduler(limit)
    scheduler.schedule(partitionedTask)


def main():
    if len(sys.argv) < 8:
        raise Exception("At least three options are needed")

    taskSetFile = sys.argv[1]

    heuristic, sort, limit, cores = None, None, None, 1
    for i in range((len(sys.argv)) // 2 - 1):
        option = sys.argv[i * 2 + 2]
        value = sys.argv[i * 2 + 3]

        if option == "-h" and value in ["ff", "wf", "bf", "nf"]:
            heuristic = value

        elif option == "-s" and value in ["iu", "du"]:
            sort = value

        elif option == "-l" and int(value) > 0:
            limit = int(value)

        elif option == "-m" and int(value) > 0:
            cores = int(value)
        else:
            raise Exception("Unknown option detected")

    if heuristic is not None and sort is not None and limit is not None:
        run(taskSetFile, heuristic, sort, limit, cores)
    else:
        raise Exception("Mandatory option not defined")


if __name__ == '__main__':
    main()
