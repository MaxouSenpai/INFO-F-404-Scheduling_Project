from Task import Task


class TaskParser:
    """TaskParser Util"""

    @staticmethod
    def parse(taskFile):
        """
        Parse the tasks contained in the specified file
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
