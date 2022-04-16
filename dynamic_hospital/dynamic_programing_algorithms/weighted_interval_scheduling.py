class Job:
    def __init__(self, start, finish, profit):
        self.start = start
        self.finish = finish
        self.profit = profit

    def __repr__(self):
        return str((self.start, self.finish, self.profit))


def findMaxProfitJobs(jobs):

    print("entrei na função")

    if not jobs:
        return 0

    jobs.sort(key=lambda x: x.start)

    n = len(jobs)

    tasks = [[] for _ in range(n)]

    maxProfit = [0] * n

    for i in range(n):
        for j in range(i):
            if jobs[j].finish <= jobs[i].start and maxProfit[i] < maxProfit[j]:
                tasks[i] = tasks[j].copy()
                maxProfit[i] = maxProfit[j]

        tasks[i].append(i)
        maxProfit[i] += jobs[i].profit

    index = 0
    for i in range(1, n):
        if maxProfit[i] > maxProfit[index]:
            index = i

    print('The jobs involved in the maximum profit are ', end='')
    for i in tasks[index]:
        print(jobs[i], end=' ')
