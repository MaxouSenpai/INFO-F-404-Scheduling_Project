import sys

from Partitioner import Partitioner
from TaskParser import TaskParser
from EDFScheduler import EDFScheduler


def run(taskSetFile, heuristic, sort, limit, cores):
    partitioner = Partitioner(heuristic, sort, cores)
    tasks = TaskParser.parse(taskSetFile)
    partitionedTask = partitioner.partition(tasks)

    scheduler = EDFScheduler(limit)
    timelines = scheduler.schedule(partitionedTask)

    prettyPrintTasks(taskSetFile, tasks)
    print()
    prettyPrintOptions(heuristic, sort, limit, cores)
    print()
    prettyPrintPartitions(partitionedTask)
    print()
    prettyPrintTimelines(timelines)


def prettyPrintTasks(taskSetFile, tasks):
    print("The tasks in " + taskSetFile + " :")
    for task in tasks:
        print("\t" + str(task))


def prettyPrintOptions(heuristic, sort, limit, cores):
    print("The options : ")
    print("\tHeuristic : ", end="")
    if heuristic == "ff":
        print("first fit")
    elif heuristic == "wf":
        print("worst fit")
    elif heuristic == "bf":
        print("best fit")
    elif heuristic == "nf":
        print("next fit")
    else:
        print("unknown")

    print("\tSort : ", end="")
    if sort == "du":
        print("decreasing utilisation")
    elif sort == "iu":
        print("increasing utilisation")
    else:
        print("unknown")

    print("\tLimit : {}".format(limit))

    print("\tCores : {}".format(cores))


def prettyPrintPartitions(partitions):
    print("The partitions :")
    for c in range(len(partitions)):
        print("\tCore {} has ".format(c), end="")
        print(" and ".join(t.str() for t in sorted(partitions[c], key=lambda t: t.getID())))


def prettyPrintTimelines(timelines):
    print("The EDF scheduling :")
    for i in range(len(timelines)):
        timelines[i].sort()
        print("\tCore {} :".format(i))
        print("\t\t" + str(timelines[i]).replace("\n", "\n\t\t"))


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
