from EDFScheduler import EDFScheduler


class Partitioner:
    """Partitioner Object"""

    def __init__(self, heuristic, sort, cores):
        """
        Construct the partitioner
        :param heuristic: the heuristic method
        :param sort: the sorting method
        :param cores: the number of cores
        """
        self.heuristic = heuristic
        self.sort = sort
        self.cores = cores

    def partition(self, tasks):
        """
        Run the partitioner
        :param tasks: the tasks
        :return: the partitioned tasks
        """

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

    def firstFit(self, tasks):
        """
        Run the first fit method
        :param tasks: the tasks
        :return: the partitioned tasks
        """
        partitionedTasks = [[] for _ in range(self.cores)]
        for task in tasks:
            i = 0
            placed = False
            while i < self.cores and not placed:
                if EDFScheduler.isSchedulable(partitionedTasks[i] + [task]):
                    partitionedTasks[i].append(task)
                    placed = True
                i += 1
            if not placed:
                raise Exception("Can't be partitioned")

        return partitionedTasks

    def worstFit(self, tasks):
        """
        Run the worst fit method
        :param tasks: the tasks
        :return: the partitioned tasks
        """
        #  sort by lowest utilisation factor
        partitionedTasks = [[] for _ in range(self.cores)]
        for task in tasks:
            partitionedTasks.sort(key=lambda ts: EDFScheduler.getUtilisationFactor(ts))
            i = 0
            placed = False
            while i < self.cores and not placed:
                if EDFScheduler.isSchedulable(partitionedTasks[i] + [task]):
                    partitionedTasks[i].append(task)
                    placed = True
                i += 1
            if not placed:
                raise Exception("Can't be partitioned")

        return partitionedTasks

    def bestFit(self, tasks):
        """
        Run the best fit method
        :param tasks: the tasks
        :return: the partitioned tasks
        """
        #  sort by highest utilisation factor
        partitionedTasks = [[] for _ in range(self.cores)]
        for task in tasks:
            partitionedTasks.sort(reverse=True, key=lambda ts: EDFScheduler.getUtilisationFactor(ts))
            i = 0
            placed = False
            while i < self.cores and not placed:
                if EDFScheduler.isSchedulable(partitionedTasks[i] + [task]):
                    partitionedTasks[i].append(task)
                    placed = True
                i += 1
            if not placed:
                raise Exception("Can't be partitioned")

        return partitionedTasks

    def nextFit(self, tasks):
        """
        Run the next fit method
        :param tasks: the tasks
        :return: the partitioned tasks
        """
        #  close processor and take the next one
        partitionedTasks = [[] for _ in range(self.cores)]
        lastUsedCore = 0
        for task in tasks:
            i = lastUsedCore
            placed = False
            while i < self.cores and not placed:
                if EDFScheduler.isSchedulable(partitionedTasks[i] + [task]):
                    partitionedTasks[i].append(task)
                    placed = True
                else:
                    i += 1
            lastUsedCore = i
            if not placed:
                raise Exception("Can't be partitioned")

        return partitionedTasks

    def sortUtilisation(self, partitionedTasks):
        """
        Sort the partitioned tasks given by their utilisation factor
        The sort depends on the sorting option chosen
        :param partitionedTasks: the partitioned tasks
        """
        partitionedTasks.sort(reverse=self.sort == "du", key=lambda core: sum(t.getWCET() for t in core))
