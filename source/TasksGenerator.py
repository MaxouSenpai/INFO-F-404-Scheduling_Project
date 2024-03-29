import sys
import random


class TasksGenerator:
    """
    This class represents a generator of random synchronous systems of tasks with constrained deadlines.
    """
    def __init__(self, tasksNumber, periodRange, utilisationFactorRange):
        """
        Construct the TasksGenerator.
        :param tasksNumber: the number of tasks to generate
        :param periodRange: the range of the periods of the tasks
        :param utilisationFactorRange: the range of the utilisation factors of the tasks
        """
        self.periodRange = periodRange
        self.tasksNumber = tasksNumber
        self.utilisationFactorRange = utilisationFactorRange

    def generate(self, outputFile):
        """
        Generate a random synchronous system of tasks with constrained deadlines.
        :param outputFile: the file on which the tasks have to be written
        """
        tasks = []
        for i in range(self.tasksNumber):
            offset = 0
            period = random.randint(self.periodRange[0], self.periodRange[1])
            lowLimit = int(self.utilisationFactorRange[0] * period)
            # The low limit should be rounded to the next integer
            if (self.utilisationFactorRange[0] * period) % 10 != 0:
                lowLimit += 1
            upLimit = int(self.utilisationFactorRange[1] * period)
            wcet = random.randint(lowLimit, upLimit)
            deadline = random.randint(wcet, period)
            tasks.append([offset, wcet, deadline, period])
        TasksGenerator.writeTasksToFile(tasks, outputFile)

    @staticmethod
    def writeTasksToFile(tasks, outputFile):
        """
        Write the specified tasks to the specified file.
        :param tasks: the tasks to write
        :param outputFile: the file on which the tasks have to be written
        """
        with open(outputFile, "w") as file:
            for task in tasks:
                file.write("{} {} {} {}\n".format(task[0], task[1], task[2], task[3]))


def run(tasksNumber, periodRange, utilisationFactorRange, outputFile):
    """
    Run the generator with the specified options
    :param tasksNumber: the number of tasks to be generated
    :param periodRange: the range of the periods of the tasks
    :param utilisationFactorRange: the range of the utilisation factors of the tasks
    :param outputFile: the file on which the tasks have to be written
    :return:
    """
    tasksGenerator = TasksGenerator(tasksNumber, periodRange, utilisationFactorRange)
    tasksGenerator.generate(outputFile)
    print("The tasks have successfully been generated and written on the output file")


def main():
    """
    Verify that the generator has all the required options and then launch it if so.
    """
    if len(sys.argv) != 9:  # pythonFilename + options (4*2)
        raise Exception("Not the right amount of arguments")

    utilisationFactorRange, periodRange, tasksNumber, outputFile = None, None, None, None
    try:
        for i in range(4):
            option = sys.argv[i * 2 + 1]
            value = sys.argv[i * 2 + 2]

            if option == "-n":
                tasksNumber = int(value)

            elif option == "-p":
                lim = value.split(",")
                periodRange = (int(lim[0]), int(lim[1]))

            elif option == "-u":
                lim = value.split(",")
                utilisationFactorRange = (float(lim[0]), float(lim[1]))

            elif option == "-o":
                outputFile = value

        if tasksNumber is None or periodRange is None or utilisationFactorRange is None or outputFile is None:
            raise Exception("Mandatory option(s) not defined")

        run(tasksNumber, periodRange, utilisationFactorRange, outputFile)

    except:
        raise Exception("Problem(s) detected in the options")


if __name__ == "__main__":
    main()
