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

    def getID(self):
        return self.id

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

        self.sortUtilisation(partitionedTasks)

        return partitionedTasks

    #  Task: WCET Deadline

    def firstFit(self, tasks):
        return [tasks]

    def worstFit(self, tasks):
        return [tasks]

    def bestFit(self, tasks):
        return [tasks]

    def nextFit(self, tasks):
        return [tasks]

    def sortUtilisation(self, partitionedTasks):
        partitionedTasks.sort(reverse=self.sort == "du", key=lambda core: sum(t.getWCET() for t in core))


class CorePartition:
    def __init__(self):
        self.tasks = []


class EDFScheduler:
    def __init__(self, timeLimit):
        self.timeLimit = timeLimit

    def schedule(self, partitionedTasks):
        print("Time limit : " + str(self.timeLimit))
        print(partitionedTasks)

        for i in range(len(partitionedTasks)):
            self.scheduleSingleCore(partitionedTasks[i], i)

    def scheduleSingleCore(self, tasks, no):
        print("Core : " + str(no))
        t = 0
        jobs = [Job(j) for j in tasks]
        events = []
        currentJob = None

        while t <= self.timeLimit:
            if currentJob is not None:
                if not currentJob.isRunning():
                    currentJob = None
                else:
                    events.append([t, repr(currentJob)])

            #  Test
            """
            jobs.sort(key=lambda j: j.task.id)
            for job in jobs:
                print(str(job.getNextDeadLine()) + " ", end="")
            print()
            print("-" * 10)
            """
            if currentJob is None:  # Search a job to execute
                jobs.sort(key=lambda j: j.getNextDeadLine())
                j = 0

                while j < len(jobs) and currentJob is None:
                    if jobs[j].canRun(t):
                        jobs[j].run()
                        currentJob = jobs[j]
                        events.append([t, repr(currentJob)])
                    j += 1

                if currentJob is None:  # If no job found
                    events.append([t, "idle"])

            for job in jobs:
                job.addTimeUnit()
            t += 1

        for e in events:
            print(e)


class Job:
    def __init__(self, task):
        self.task = task
        self.running = False
        self.executionTime = 0
        self.idleTime = 0
        self.no = 0  # Number of times that the job ran

    def addTimeUnit(self):
        if self.running:
            self.executionTime += 1
            if self.executionTime == self.task.getWCET():  # Finished
                self.running = False
                self.no += 1

        else:
            self.idleTime += 1

        if self.executionTime + self.idleTime == self.task.getPeriod():
            self.executionTime = 0
            self.idleTime = 0

    def getNextDeadLine(self):
        return self.task.getOffset() + self.task.getPeriod() * self.no + self.task.getDeadline()

    def run(self):
        self.running = True

    def canRun(self, t):
        return self.task.getOffset() <= t and self.executionTime == 0

    def isRunning(self):
        return self.running

    def __repr__(self):
        return "T{}|J{}".format(self.task.getID(), self.no)


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
