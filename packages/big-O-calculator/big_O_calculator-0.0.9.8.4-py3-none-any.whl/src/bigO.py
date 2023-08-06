import math
from random import randrange
from time import time

"""Big-O calculator

usage:
    bigO = bigO()
	bigO.test("someSort", "random")
	
"""
class bigO:
    def __init__(self):
        self.coef = 0.0
        self.rms = 0.0
        self.cplx = 0
        self._ = 0
        self.O1 = 1
        self.ON = 2
        self.ON2 = 3
        self.ON3 = 4
        self.OLogN = 5
        self.ONLogN = 6
        self.OLambda = 7
        self.fitCurves = [self.O1, self.ON, self.ON2, self.ON3, self.OLogN, self.ONLogN]

    def str(self):
        return self.complexity2str(self.cplx)

    def complexity2str(self, cplx):
        def switch(cplx):
            return {
                self.ON: "O(N)",
                self.ON2: "O(N^2)",
                self.ON3: "O(N^3)",
                self.OLogN: "O(lg(N)",
                self.ONLogN: "O(Nlg(N))",
                self.O1: "O(1)",
            }.get(cplx, "f(n)")

        return switch(cplx)

    def fittingCurve(self, cplx):
        def calc_ON(n):
            return n

        def calc_ON2(n):
            return n * n

        def calc_ON3(n):
            return n * n * n

        def calc_OLogN(n):
            return math.log2(n)

        def calc_ONLogN(n):
            return n * math.log2(n)

        def calc_O1(_):
            return 1.0

        def switch(cplx):
            return {
                self.O1: calc_O1,
                self.ON: calc_ON,
                self.ON2: calc_ON2,
                self.ON3: calc_ON3,
                self.OLogN: calc_OLogN,
                self.ONLogN: calc_ONLogN,
            }.get(cplx, calc_O1)

        return switch(cplx)

    def minimalLeastSq(self, arr, times, function):
        # sigmaGn = 0.0
        sigmaGnSquared = 0.0
        sigmaTime = 0.0
        sigmaTimeGn = 0.0

        floatN = float(len(arr))

        for i in range(len(arr)):
            gnI = function(arr[i])
            # sigmaGn = gnI
            sigmaGnSquared += gnI * gnI
            sigmaTime += times[i]
            sigmaTimeGn += times[i] * gnI

        result = bigO()
        result.cplx = self.OLambda

        result.coef = sigmaTimeGn / sigmaGnSquared

        rms = 0.0
        for i in range(len(arr)):
            fit = result.coef * function(arr[i])
            rms += math.pow(times[i] - fit, 2)

        mean = sigmaTime / floatN
        result.rms = math.sqrt(rms / floatN) / mean

        return result

    def estimate(self, n, times):
        bestFit = bigO()

        if len(n) != len(times):
            return bestFit, "Length mismatch between n and times"
        if len(n) < 2:
            return bestFit, "Need at least 2 runs"

        bestFit = self.minimalLeastSq(n, times, self.fittingCurve(self.O1))
        bestFit.cplx = self.O1

        for fit in self.fitCurves:
            currentFit = self.minimalLeastSq(n, times, self.fittingCurve(fit))
            if currentFit.rms < bestFit.rms:
                bestFit = currentFit
                bestFit.cplx = fit

        return bestFit, None

    def test(self, functionName, array):
        """Big-O calculator

        Args:
            functionName ([string]): function name to call
            array ([string]): "random", "sorted", "reversed", "partial"
        """   
        def genRandomArray(size):
            array = []
            for _ in range(size):
                array.append(randrange(-size, size))
            return array

        def genSortedArray(size):
            array = []
            for value in range(size):
                array.append(value)
            return array

        def genReversedArray(size):
            array = []
            for value in reversed(range(size)):
                array.append(value)
            return array

        def genPartialArray(size):
            array = genRandomArray(size)
            sorted_array = genSortedArray(size)

            array[size // 4 : size // 2] = sorted_array[size // 4 : size // 2]
            return array

        bigOtest = bigO()

        sizes = [10, 100, 1000, 10000]
        maxIter = 5
        times = []

        print(f"Running {functionName}({array} array)...")
        for size in sizes:
            timeTaken = 0.0
            nums = []

            if array == "random":
                nums = genRandomArray(size)
            elif array == "sorted":
                nums = genSortedArray(size)
            elif array == "partial":
                nums = genPartialArray(size)
            elif array == "reversed":
                nums = genReversedArray(size)
            else:  # default = random array
                nums = genRandomArray(size)

            currentIter = 0

            while currentIter < maxIter:
                start = time()
                globals()[functionName](nums)
                end = time()
                timeTaken += end - start
                currentIter += 1

            timeTaken /= maxIter
            times.append(timeTaken)

        print(f"Completed {functionName}({array} array)...")

        complexity, _ = bigOtest.estimate(sizes, times)

        return complexity.str(), _
