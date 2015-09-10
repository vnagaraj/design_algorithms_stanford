__author__ = 'VGN'


class BruteForceCountInversions:

    def __init__(self, input):
        self.input = input

    def count_inversions(self):
        running_count = 0
        for i in range(0, len(self.input)):
            for j in range(i+1, len(self.input)):
                if self.input[i] > self.input[j]:
                    running_count += 1
        return running_count


class CountInversions:
    def __init__(self, input):
        # list allocation done only once
        self.input = input
        self.aux = input[:]

    def count_inversions(self):
        return self.sort_count(self.input, 0, len(self.input)-1)

    def count_split_inversions(self, input, low, middle, high):
        split_inversions_count = 0
        # copy elements from input array to aux array in range low to hi
        for i in range(low, high+1):
            self.aux[i] = input[i]
        i = low
        j = middle + 1
        for k in range(low, high + 1):
            if i > middle: # i pointer falling off ( first half completed)
                input[k] = self.aux[j]
                j=j+1
            elif j > high: # j pointer falling off ( second half completed)
                input[k] = self.aux[i]
                i=i+1
            elif self.aux[i] < self.aux[j]:
                input[k] = self.aux[i]
                i = i +1
            elif self.aux[j] < self.aux[i]:
                input[k] = self.aux[j]
                # printing split inversions
                """
                for l in range(i, middle+1):
                    print (self.aux[l], self.aux[j])
                """
                j = j + 1
                split_inversions_count += middle+1 - i

        return split_inversions_count

    def sort_count(self, input, low, high):
        if low >= high:
            return 0
        middle = (high - low)/2 + low
        x = self.sort_count(input, low, middle)
        y = self.sort_count(input, middle + 1, high)
        z = self.count_split_inversions(input, low, middle, high)
        return x + y + z;



input = [9, 12, 3, 1, 6, 8, 2, 5, 14, 13, 11, 7, 10, 4, 0 ]

print "count inversions " + str(CountInversions(input).count_inversions())

input = [9, 12, 3, 1, 6, 8, 2, 5, 14, 13, 11, 7, 10, 4, 0 ]
print "count inversions Brute Force " + str(BruteForceCountInversions(input).count_inversions())



