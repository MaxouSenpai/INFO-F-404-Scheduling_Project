import sys


class TasksGenerator:
    """
    This class represents a generator of random synchronous systems of tasks with constrained deadlines.
    """
    def __init__(self, utilisationFactor, tasksNumber):
        self.utilisationFactor = utilisationFactor
        self.tasksNumber = tasksNumber

    def generate(self, outputFile):
        """
        Generate a synchronous system of tasks with constrained deadlines.
        :param outputFile: the file on which the tasks have to be written
        """
        tasks = [[0, 0, 0, 0] for _ in range(self.tasksNumber)]
        # TODO random
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


def run(utilisationFactor, tasksNumber, outputFile):
    """
    Run the generator with the specified options
    :param utilisationFactor: the sum of the utilisation factors of all the tasks
    :param tasksNumber: the number of tasks to be generated
    :param outputFile: the file on which the tasks have to be written
    :return:
    """
    tasksGenerator = TasksGenerator(utilisationFactor, tasksNumber)
    tasksGenerator.generate(outputFile)
    print("The tasks have successfully been generated and written to the output file")


def main():
    """
    Verify that the generator has all the required options and then launch it if so.
    """
    # TasksGenerator -u float -n int -o output
    if len(sys.argv) != 7:  # filename + options (3*2)
        raise Exception("Not the right amount of arguments")

    utilisationFactor, tasksNumber, outputFile = None, None, None

    for i in range(3):
        option = sys.argv[i * 2 + 1]
        value = sys.argv[i * 2 + 2]

        if option == "-u":
            utilisationFactor = float(value)

        elif option == "-n":
            tasksNumber = int(value)

        elif option == "-o":
            outputFile = value

    if utilisationFactor is not None and tasksNumber is not None and outputFile is not None:
        run(utilisationFactor, tasksNumber, outputFile)
    else:
        raise Exception("Mandatory option(s) not defined")


if __name__ == "__main__":
    main()
