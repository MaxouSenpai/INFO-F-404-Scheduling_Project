import sys
import random


class TasksGenerator:
    """
    This class represents a generator of random synchronous systems of tasks with constrained deadlines.
    """
    def __init__(self, tasksNumber, period, utilisationFactor):
        """
        Construct the TasksGenerator.
        :param tasksNumber: the number of tasks to generate
        :param period: the range of the periods of the tasks
        :param utilisationFactor: the range of the utilisation factors of the tasks
        :param period: the range of the periods of the tasks
        """
        self.utilisationFactor = utilisationFactor
        self.period = period
        self.tasksNumber = tasksNumber

    def generate(self, outputFile):
        """
        Generate a random synchronous system of tasks with constrained deadlines.
        :param outputFile: the file on which the tasks have to be written
        """
        tasks = []
        for i in range(self.tasksNumber):
            offset = 0
            period = random.randint(self.period[0], self.period[1])
            lowLimit = int(self.utilisationFactor[0] * period)
            # The low limit should be rounded to the next integer
            if (self.utilisationFactor[0] * period) % 10 != 0:
                lowLimit += 1
            upLimit = int(self.utilisationFactor[1] * period)
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


def run(tasksNumber, period, utilisationFactor, outputFile):
    """
    Run the generator with the specified options
    :param tasksNumber: the number of tasks to be generated
    :param period: the range of the periods of the tasks
    :param utilisationFactor: the range of the utilisation factors of the tasks
    :param outputFile: the file on which the tasks have to be written
    :return:
    """
    tasksGenerator = TasksGenerator(tasksNumber, period, utilisationFactor)
    tasksGenerator.generate(outputFile)
    print("The tasks have successfully been generated and written to the output file")


def main():
    """
    Verify that the generator has all the required options and then launch it if so.
    """
    if len(sys.argv) != 9:  # pythonFilename + options (4*2)
        raise Exception("Not the right amount of arguments")

    utilisationFactor, period, tasksNumber, outputFile = None, None, None, None
    try:
        for i in range(4):
            option = sys.argv[i * 2 + 1]
            value = sys.argv[i * 2 + 2]

            if option == "-n":
                tasksNumber = int(value)

            elif option == "-p":
                lim = value.split(",")
                period = (int(lim[0]), int(lim[1]))

            elif option == "-u":
                lim = value.split(",")
                utilisationFactor = (float(lim[0]), float(lim[1]))

            elif option == "-o":
                outputFile = value

        if tasksNumber is None or period is None or utilisationFactor is None or outputFile is None:
            raise Exception("Mandatory option(s) not defined")

        run(tasksNumber, period, utilisationFactor, outputFile)

    except:
        raise Exception("Problem(s) detected in the options")


if __name__ == "__main__":
    main()
