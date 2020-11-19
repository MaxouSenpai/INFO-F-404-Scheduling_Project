import sys

from Partitioner import Partitioner
from EDFScheduler import EDFScheduler
from Task import Task


def run(taskSetFile, heuristic, sort, limit, cores):
    """
    Run the program with the specified parameters and
    print the results in a nice and readable style.
    :param taskSetFile: the task set file
    :param heuristic: the heuristic option
    :param sort: the sorting option
    :param limit: the time limit
    :param cores: the number of cores
    """
    partitioner = Partitioner(heuristic, sort, cores)
    tasks = parseTasks(taskSetFile)

    try:
        partitionedTask = partitioner.partition(tasks)

    except Exception:
        print("Error : It cannot be partitioned!")
        return

    edfScheduler = EDFScheduler()
    timelines = edfScheduler.scheduleAll(partitionedTask, limit)

    prettyPrintTasks(taskSetFile, tasks)
    print()
    prettyPrintOptions(heuristic, sort, limit, cores)
    print()
    prettyPrintPartitions(partitionedTask)
    print()
    prettyPrintTimelines(timelines)


def prettyPrintTasks(taskSetFile, tasks):
    """
    Print the partitions in a nice and readable style.
    :param taskSetFile: the task set file
    :param tasks: the tasks
    """
    print("The tasks in " + taskSetFile + " :")
    tasks.sort(key=lambda t: t.getID())
    for task in tasks:
        print("\t" + task.asDetailedString())


def prettyPrintOptions(heuristic, sort, limit, cores):
    """
    Print the options in a nice and readable style.
    :param heuristic: the heuristic option
    :param sort: the sorting option
    :param limit: the time limit option
    :param cores: the number of cores
    """
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

    print("\tTime limit : {}".format(limit))

    print("\tCores : {}".format(cores))

    print("\tScheduler : {}".format("EDF"))


def prettyPrintPartitions(partitions):
    """
    Print the partitions in a nice and readable style.
    :param partitions: the partitions
    """
    print("The partitions :")
    for c in range(len(partitions)):
        print("\tCore {} has ".format(c), end="")
        if len(partitions[c]) > 0:
            print(" and ".join(t.asString() for t in sorted(partitions[c], key=lambda t: t.getID())))
        else:
            print("no task")


def prettyPrintTimelines(timelines):
    """
    Print the timelines in a nice and readable style.
    :param timelines: the timelines
    """
    print("The EDF scheduling :")
    for i in range(len(timelines)):
        print("\tCore {} :".format(i))
        print("\t\t" + timelines[i].asString().replace("\n", "\n\t\t"))


def parseTasks(taskFile):
    """
    Parse the tasks contained in the specified file.
    :param taskFile: the file containing the tasks
    :return: the list of the tasks contained in the file
    """
    tasks = []
    with open(taskFile) as file:
        tid = 0
        for line in file:
            attr = line.split(" ")
            if len(attr) == 4:
                tasks.append(Task(int(attr[0]), int(attr[1]), int(attr[2]), int(attr[3]), tid))
            tid += 1
    return tasks


def main():
    """
    Verify that the program has all the required options and then launch it if so.
    """
    if len(sys.argv) < 8:  # 1 (main.py) + 1 (file) + 3 * 2 (option names + value) = 8 (at least)
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
        raise Exception("Mandatory option(s) not defined")


if __name__ == '__main__':
    main()
