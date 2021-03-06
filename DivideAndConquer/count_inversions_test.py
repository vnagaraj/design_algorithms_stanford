__author__ = 'VGN'
import unittest
import logging
from count_inversions import CountInversions



class TestCountInversions(unittest.TestCase):
    def test1(self):
        input = [1, 3, 5, 2, 4, 6]
        x = CountInversions(input).count_inversions()
        self.assertTrue(x == 3)

    def test2(self):
        input = [1, 5, 3, 2, 4]
        x = CountInversions(input).count_inversions()
        self.assertTrue(x == 4)

    def test3(self):
        input = [5, 4, 3, 2, 1]
        x = CountInversions(input).count_inversions()
        self.assertTrue(x == 10)

    def test4(self):
        input = [1, 6, 3, 2, 4, 5]
        x = CountInversions(input).count_inversions()
        self.assertTrue(x == 5)

    def test5(self):
        input = [9, 12, 3, 1, 6, 8, 2, 5, 14, 13, 11, 7, 10, 4, 0 ]
        print len(input)
        x = CountInversions(input).count_inversions()
        self.assertTrue(x == 56)

    def test6(self):
        input = [37, 7, 2, 14, 35, 47, 10, 24, 44, 17, 34, 11, 16, 48, 1, 39, 6,
                 33, 43, 26, 40, 4, 28, 5, 38, 41, 42, 12, 13, 21, 29, 18, 3, 19,
                 0, 32, 46, 27, 31, 25, 15, 36, 20, 8, 9, 49, 22, 23, 30, 45]
        x = CountInversions(input).count_inversions()
        self.assertTrue(x == 590)

    def test7(self):
        input = [4, 80, 70, 23, 9, 60, 68, 27, 66, 78, 12, 40, 52, 53, 44, 8, 49, 28,
                 18, 46, 21, 39, 51, 7, 87, 99, 69, 62, 84, 6, 79, 67, 14, 98, 83, 0,
                 96, 5, 82, 10, 26, 48, 3, 2, 15, 92, 11, 55, 63, 97, 43, 45, 81, 42,
                 95, 20, 25, 74, 24, 72, 91, 35, 86, 19, 75, 58, 71, 47, 76, 59, 64,
                 93, 17, 50, 56, 94, 90, 89, 32, 37, 34, 65, 1, 73, 41, 36, 57, 77,
                 30, 22, 13, 29, 38, 16, 88, 61, 31, 85, 33, 54]
        x = CountInversions(input).count_inversions()
        self.assertTrue(x == 2372)

    def test8(self):
        input = [1, 48, 22, 4, 25, 28, 41, 31, 49, 46, 20, 12, 5, 16, 45, 10, 18, 11, 44,
                 9, 36, 6, 27, 14, 30, 33, 43, 50, 2, 39, 17, 24, 29, 42, 26, 37, 40, 23,
                 32, 34, 13, 38, 7, 3, 19, 35, 15, 21, 8, 47]
        x = CountInversions(input).count_inversions()
        self.assertTrue(x == 614)

    def test9(self):
        input = [96, 44, 48, 11, 68, 50, 27, 39, 87, 33, 67, 100, 54, 25, 59, 65, 26, 4, 51, 82,
                 86, 63, 2, 3, 71, 21, 79, 85, 73, 15, 47, 45, 18, 92, 17, 78, 74, 13, 37, 8, 42,
                 72, 41, 80, 98, 16, 6, 10, 56, 95, 88, 62, 19, 46, 28, 34, 49, 76, 23, 83, 84,
                 75, 66, 38, 55, 31, 30, 99, 90, 70, 22, 64, 12, 43, 35, 53, 93, 89, 24, 1, 52,
                 77, 97, 5, 91, 57, 20, 7, 32, 94, 60, 14, 69, 9, 29, 58, 40, 61, 81, 36]
        x = CountInversions(input).count_inversions()
        self.assertTrue(x == 2489)

    def test10(self):
        input = [49, 105, 93, 107, 90, 125, 16, 144, 141, 48, 58, 150, 62, 47, 108, 126, 92, 35, 20,
                 41, 46, 70, 132, 96, 39, 13, 67, 117, 124, 136, 45, 122, 29, 6, 31, 21, 18, 28, 146,
                 69, 3, 44, 138, 101, 86, 5, 94, 52, 84, 76, 51, 7, 27, 99, 100, 113, 109, 110, 116, 40,
                 22, 50, 59, 130, 15, 66, 139, 97, 9, 34, 112, 10, 115, 37, 53, 38, 64, 121, 120, 17, 127,
                 56, 80, 42, 23, 55, 145, 65, 131, 2, 104, 78, 4, 123, 114, 89, 72, 71, 82, 111, 54, 85,
                 143, 134, 128, 63, 118, 149, 24, 43, 91, 129, 26, 87, 81, 77, 57, 25, 79, 147, 60, 102,
                 74, 88, 148, 61, 142, 32, 137, 11, 36, 140, 98, 106, 95, 1, 30, 135, 119, 103, 14, 33, 73,
                 75, 68, 12, 19, 133, 83, 8]
        x = CountInversions(input).count_inversions()
        self.assertTrue(x == 5524)

    def test11(self):
        input = [76, 85, 59, 142, 67, 51, 133, 64, 42, 128, 9, 153, 169, 114, 193, 162, 90, 77, 14, 154, 151,
                 182, 18, 160, 197, 26, 143, 178, 137, 166, 1, 74, 152, 122, 185, 10, 78, 107, 84, 113, 116,
                 28, 175, 124, 129, 89, 30, 29, 163, 49, 40, 101, 66, 19, 80, 119, 135, 57, 38, 104, 73, 32,
                 146, 2, 91, 99, 190, 58, 132, 23, 194, 75, 167, 79, 123, 112, 199, 131, 60, 55, 47, 174, 17,
                 168, 52, 155, 109, 200, 161, 136, 195, 111, 25, 71, 145, 88, 24, 81, 186, 16, 130, 179, 68, 65,
                 83, 156, 53, 148, 4, 196, 33, 50, 3, 94, 34, 45, 36, 147, 35, 70, 62, 69, 191, 141, 22, 46, 183,
                 126, 87, 13, 159, 103, 127, 144, 8, 11, 41, 189, 198, 54, 56, 108, 176, 106, 173, 97, 21, 164, 98,
                 172, 171, 170, 149, 110, 138, 31, 125, 63, 82, 192, 39, 92, 95, 15, 7, 105, 187, 180, 5, 6, 44, 102,
                 134, 188, 181, 139, 184, 177, 12, 115, 61, 165, 37, 140, 100, 157, 20, 150, 43, 117, 120, 48, 27,
                 121, 86, 96, 158, 72, 118, 93]
        x = CountInversions(input).count_inversions()
        self.assertTrue(x == 9945)

    def test12(self):
        input = list()
        with open("integerArray.txt", "r") as ins:
            for line in ins:
                input.append(int(line))
        x = CountInversions(input).count_inversions()
        print x
        logging.info("Value is {}".format(x))

if __name__ == '__main__':
    unittest.main()