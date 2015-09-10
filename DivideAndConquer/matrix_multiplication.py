__author__ = 'VGN'

import unittest
import random


class RowColMisMatch(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class Matrix(object):
    def __init__(self, matrix):
        self.matrix = matrix
        # validate matrix
        row_count = len(self.matrix)
        for item in self.matrix:
            if len(item) != row_count:
                raise RowColMisMatch("rowCount and colCount should match")

    def __mul__(self, other):
        output_matrix = self._create_list(len(self.matrix), len(self.matrix))
        start_row_x = 0
        end_row_x = len(self.matrix) - 1
        start_col_x = 0
        end_col_x = len(self.matrix) - 1
        start_row_y = 0
        end_row_y = len(other.matrix) - 1
        start_col_y = 0
        end_col_y = len(other.matrix) - 1
        x_dimension = [start_row_x, end_row_x, start_col_x, end_col_x]
        y_dimension = [start_row_y, end_row_y, start_col_y, end_col_y]
        self.brute_force_matrix_multiplication(self.matrix, other.matrix, x_dimension, y_dimension, output_matrix)
        return Matrix(output_matrix)

    def __repr__(self):
        return repr(self.matrix)

    def __eq__(self, other):
        if other is None:
            return False
        x = self.matrix
        y = other.matrix
        if len(x) != len(y):
            return False
        if len(x[0]) != len(y[0]):
            return False
        for i in range(0, len(x)):
            for j in range(0, len(x[0])):
                if x[i][j] != y[i][j]:
                    return False
        return True

    def _create_list(self, row_length, col_length):
        z = list()
        for i in range(row_length):
            sub_list = list()
            for j in range(col_length):
                sub_list.append(0)
            z.append(sub_list)
        return z

    def brute_force_matrix_multiplication(self, x, y, x_dimension, y_dimension, output_matrix):
        start_row_x = x_dimension[0]
        end_row_x = x_dimension[1]
        start_col_x = x_dimension[2]
        end_col_x = x_dimension[3]
        start_row_y = y_dimension[0]
        end_row_y = y_dimension[1]
        start_col_y = y_dimension[2]
        end_col_y = y_dimension[3]
        output_row = 0
        output_col = 0
        prod = 0
        for i in range(start_row_x, end_row_x + 1):
            for j in range(start_col_y, end_col_y + 1):
                l = start_row_y
                for k in range(start_col_x, end_col_x + 1):
                    prod = x[i][k] * y[l][j]
                    output_matrix[output_row][output_col] += prod
                    l += 1
                output_col += 1
            output_row += 1
            output_col = 0

    def divide_conquer_matrix_multiplication(self, other):
        x = self.matrix
        y = other.matrix
        length = len(self.matrix)
        # output matrix
        self.z = self._create_list(length, length)
        if length % 2 != 0:  # in case matrix is of odd length
            length += 1
        # 8 empty n/2 matrixes
        a = (length / 2, length / 2)
        b = (length / 2, len(self.matrix) - length / 2)
        c = (len(self.matrix) - length / 2, length / 2)
        d = (len(self.matrix) - length / 2, len(self.matrix) - length / 2)
        # same dimensions for B
        e = a
        f = b
        g = c
        h = d
        self.ae = self._create_list(a[0], e[1])
        self.bg = self._create_list(b[0], g[1])
        self.af = self._create_list(a[0], f[1])
        self.bh = self._create_list(b[0], h[1])
        self.ce = self._create_list(c[0], e[1])
        self.dg = self._create_list(d[0], g[1])
        self.cf = self._create_list(c[0], f[1])
        self.dh = self._create_list(d[0], h[1])
        start_row_x = 0
        end_row_x = len(self.matrix) - 1
        start_col_x = 0
        end_col_x = len(self.matrix) - 1
        start_row_y = 0
        end_row_y = len(y) - 1
        start_col_y = 0
        end_col_y = len(y) - 1
        x_dimension = [start_row_x, end_row_x, start_col_x, end_col_x]
        y_dimension = [start_row_y, end_row_y, start_col_y, end_col_y]
        self._recursive_divide_conquer(x, y, x_dimension, y_dimension)
        return Matrix(self.z)

    def _recursive_divide_conquer(self, x, y, x_dimension, y_dimension, output=None):
        start_row_x = x_dimension[0]
        end_row_x = x_dimension[1]
        start_col_x = x_dimension[2]
        end_col_x = x_dimension[3]
        start_row_y = y_dimension[0]
        end_row_y = y_dimension[1]
        start_col_y = y_dimension[2]
        end_col_y = y_dimension[3]
        middle_row_x = (end_row_x - start_row_x) / 2 + start_row_x
        middle_col_x = (end_col_x - start_col_x) / 2 + start_col_x
        middle_row_y = (end_row_y - start_row_y) / 2 + start_row_y
        middle_col_y = (end_col_y - start_col_y) / 2 + start_col_y
        # base
        if end_row_x - start_row_x <= 2:  # 2* 2 matrix
            # brute force implementation
            if output != None:
                self.brute_force_matrix_multiplication(x, y, x_dimension, y_dimension, output)
                return
        # ae
        x_dimension = [start_row_x, middle_row_x, start_col_x, middle_col_x]
        y_dimension = [start_row_y, middle_row_y, start_col_y, middle_col_y]
        self._recursive_divide_conquer(x, y, x_dimension, y_dimension, self.ae)
        #bg
        x_dimension = [start_row_x, middle_row_x, middle_col_x + 1, end_col_x]
        y_dimension = [middle_row_y + 1, end_row_y, start_col_y, middle_col_y]
        self._recursive_divide_conquer(x, y, x_dimension, y_dimension, self.bg)
        # add ae and bg
        output_dimension = [start_row_x, middle_row_x, start_col_x, middle_col_x]
        matrix_list = [(self.ae, False), (self.bg, False)]
        self.add_matrix(matrix_list, output_dimension)
        #af
        x_dimension = [start_row_x, middle_row_x, start_col_x, middle_col_x]
        y_dimension = [start_row_y, middle_row_y, middle_col_y + 1, end_col_y]
        self._recursive_divide_conquer(x, y, x_dimension, y_dimension, self.af)
        #bh
        x_dimension = [start_row_x, middle_row_x, middle_col_x + 1, end_col_x]
        y_dimension = [middle_row_y + 1, end_row_y, middle_col_y + 1, end_col_y]
        self._recursive_divide_conquer(x, y, x_dimension, y_dimension, self.bh)
        # add af and bh
        output_dimension = [start_row_x, middle_row_x, middle_col_x + 1, end_col_x]
        matrix_list = [(self.af, False), (self.bh, False)]
        self.add_matrix(matrix_list, output_dimension)
        #ce
        x_dimension = [middle_row_x + 1, end_row_x, start_col_x, middle_col_x]
        y_dimension = [start_row_y, middle_row_y, start_col_y, middle_col_y]
        self._recursive_divide_conquer(x, y, x_dimension, y_dimension, self.ce)
        #dg
        x_dimension = [middle_row_x + 1, end_row_x, middle_col_x + 1, end_col_x]
        y_dimension = [middle_row_y + 1, end_row_y, start_col_y, middle_col_y]
        self._recursive_divide_conquer(x, y, x_dimension, y_dimension, self.dg)
        # add ce and dg
        output_dimension = [middle_row_x + 1, end_row_x, start_col_x, middle_col_x]
        matrix_list = [(self.ce, False), (self.dg, False)]
        self.add_matrix(matrix_list, output_dimension)
        #cf
        x_dimension = [middle_row_x + 1, end_row_x, start_col_x, middle_col_x]
        y_dimension = [start_row_y, middle_row_y, middle_col_y + 1, end_col_y]
        self._recursive_divide_conquer(x, y, x_dimension, y_dimension, self.cf)
        #dh
        x_dimension = [middle_row_x + 1, end_row_x, middle_col_x + 1, end_col_x]
        y_dimension = [middle_row_y + 1, end_row_y, middle_col_y + 1, end_col_y]
        self._recursive_divide_conquer(x, y, x_dimension, y_dimension, self.dh)
        # add cf and dh
        output_dimension = [middle_row_x + 1, end_row_x, middle_col_x + 1, end_col_x]
        matrix_list = [(self.cf, False), (self.dh, False)]
        self.add_matrix(matrix_list, output_dimension)

    def add_matrix(self, matrix_list, output_dimension, is_subtract=False):
        starting_row = output_dimension[0]
        starting_col = output_dimension[2]
        row_length = len(matrix_list[0][0])
        col_length = len(matrix_list[0][0][0])

        for i in range(row_length):
            for j in range(col_length):
                sum = 0
                for matrix_tup in matrix_list:
                    matrix = matrix_tup[0]
                    is_subtract = matrix_tup[1]
                    if is_subtract:
                        sum -= matrix[i][j]
                    else:
                        sum += matrix[i][j]
                self.z[starting_row][starting_col] = sum
                starting_col += 1
            starting_col = output_dimension[2]
            starting_row += 1

    def straussen_matrix_multiplication(self, other):
        x = self.matrix
        y = other.matrix
        n = len(self.matrix)
        self.a = self._create_list(n / 2, n / 2)
        self.f_minus_h = self._create_list(n / 2, n / 2)
        self.p1 = self._create_list(n / 2, n / 2)
        self.a_plus_b = self._create_list(n / 2, n / 2)
        self.h = self._create_list(n / 2, n / 2)
        self.p2 = self._create_list(n / 2, n / 2)
        self.c_plus_d = self._create_list(n / 2, n / 2)
        self.e = self._create_list(n / 2, n / 2)
        self.p3 = self._create_list(n / 2, n / 2)
        self.d = self._create_list(n / 2, n / 2)
        self.g_minus_e = self._create_list(n / 2, n / 2)
        self.p4 = self._create_list(n / 2, n / 2)
        self.a_plus_d = self._create_list(n / 2, n / 2)
        self.e_plus_h = self._create_list(n / 2, n / 2)
        self.p5 = self._create_list(n / 2, n / 2)
        self.b_minus_d = self._create_list(n / 2, n / 2)
        self.g_plus_h = self._create_list(n / 2, n / 2)
        self.p6 = self._create_list(n / 2, n / 2)
        self.a_minus_c = self._create_list(n / 2, n / 2)
        self.e_plus_f = self._create_list(n / 2, n / 2)
        self.p7 = self._create_list(n / 2, n / 2)
        self._straussen_recursive(x, y)
        return Matrix(self.z)

    def _straussen_recursive(self, matrix1=None, matrix2=None, output=None):
        start_row_x = 0
        end_row_x = len(matrix1) - 1
        start_col_x = 0
        end_col_x = len(matrix1[0]) - 1
        start_row_y = 0
        end_row_y = len(matrix2) - 1
        start_col_y = 0
        end_col_y = len(matrix2[0]) - 1
        middle_row_x = (end_row_x - start_row_x) / 2 + start_row_x
        middle_col_x = (end_col_x - start_col_x) / 2 + start_col_x
        middle_row_y = (end_row_y - start_row_y) / 2 + start_row_y
        middle_col_y = (end_col_y - start_col_y) / 2 + start_col_y
        # base
        if end_row_x - start_row_x <= 2:  # 2* 2 matrix
            #brute force implementation
            if output != None:
                x_dimension = [0, len(matrix1) - 1, 0, len(matrix1[0]) - 1]
                y_dimension = [0, len(matrix2) - 1, 0, len(matrix2[0]) - 1]
                self.brute_force_matrix_multiplication(matrix1, matrix2, x_dimension, y_dimension, output)
                return
        #a
        a_dimension = [start_row_x, middle_row_x, start_col_x, middle_col_x]
        self._set_matrix(a_dimension, matrix1, self.a)
        #f
        f_dimension = [start_row_y, middle_row_y, middle_col_y + 1, end_col_y]
        #h
        h_dimension = [middle_row_y + 1, end_row_y, middle_col_y + 1, end_col_y]
        self._straussen_add_subtract_matrix(f_dimension, h_dimension, matrix2, self.f_minus_h)
        # 1st recursive call to compute p1
        self._straussen_recursive(self.a, self.f_minus_h, self.p1)
        #a
        a_dimension = [start_row_x, middle_row_x, start_col_x, middle_col_x]
        #b
        b_dimension = [start_row_x, middle_row_x, middle_col_x + 1, end_col_x]
        self._straussen_add_subtract_matrix(a_dimension, b_dimension, matrix1, self.a_plus_b, True)
        self._set_matrix(h_dimension, matrix2, self.h)
        # 2nd recursive call to compute p2
        self._straussen_recursive(self.a_plus_b, self.h, self.p2)
        c_dimension = [middle_row_x + 1, end_row_x, start_col_x, middle_col_x]
        d_dimension = [middle_row_x + 1, end_row_x, middle_col_x + 1, end_col_x]
        self._straussen_add_subtract_matrix(c_dimension, d_dimension, matrix1, self.c_plus_d, True)
        e_dimension = [start_row_y, middle_row_y, start_col_y, middle_col_y]
        self._set_matrix(e_dimension, matrix2, self.e)
        # 3rd recursive call to compute p3
        self._straussen_recursive(self.c_plus_d, self.e, self.p3)
        g_dimension = [middle_row_y + 1, end_row_y, start_col_y, middle_col_y]
        self._straussen_add_subtract_matrix(g_dimension, e_dimension, matrix2, self.g_minus_e)
        self._set_matrix(d_dimension, matrix1, self.d)
        # 4th recursive call to compute p4
        self._straussen_recursive(self.d, self.g_minus_e, self.p4)
        self._straussen_add_subtract_matrix(a_dimension, d_dimension, matrix1, self.a_plus_d, True)
        self._straussen_add_subtract_matrix(e_dimension, h_dimension, matrix2, self.e_plus_h, True)
        # 5th recursive call to compute p5
        self._straussen_recursive(self.a_plus_d, self.e_plus_h, self.p5)
        self._straussen_add_subtract_matrix(b_dimension, d_dimension, matrix1, self.b_minus_d)
        self._straussen_add_subtract_matrix(g_dimension, h_dimension, matrix2, self.g_plus_h, True)
        #6th recursive call to compute p6
        self._straussen_recursive(self.b_minus_d, self.g_plus_h, self.p6)
        self._straussen_add_subtract_matrix(a_dimension, c_dimension, matrix1, self.a_minus_c)
        self._straussen_add_subtract_matrix(e_dimension, f_dimension, matrix2, self.e_plus_f, True)
        #7th recursive call to compute p7
        self._straussen_recursive(self.a_minus_c, self.e_plus_f, self.p7)
        # combine step into output array
        output_dimension = [start_row_x, middle_row_x, start_col_x, middle_col_x]
        matrix_list = [(self.p5, False), (self.p4, False), (self.p2, True), (self.p6, False)]
        self.add_matrix(matrix_list, output_dimension)
        output_dimension = [start_row_x, middle_row_x, middle_col_x + 1, end_col_x]
        matrix_list = [(self.p1, False), (self.p2, False)]
        self.add_matrix(matrix_list, output_dimension)
        output_dimension = [middle_row_x + 1, end_row_x, start_col_x, middle_col_x]
        matrix_list = [(self.p3, False), (self.p4, False)]
        self.add_matrix(matrix_list, output_dimension)
        output_dimension = [middle_row_x + 1, end_row_x, middle_col_x + 1, end_col_x]
        matrix_list = [(self.p1, False), (self.p5, False), (self.p3, True), (self.p7, True)]
        self.add_matrix(matrix_list, output_dimension)

    def _set_matrix(self, dimension, input_matrix, output_matrix):
        start_row = dimension[0]
        end_row = dimension[1]
        start_col = dimension[2]
        end_col = dimension[3]
        i = 0
        j = 0
        for row in range(start_row, end_row + 1):
            for col in range(start_col, end_col + 1):
                output_matrix[i][j] = input_matrix[row][col]
                j += 1
            i += 1
            j = 0

    def _straussen_add_subtract_matrix(self, dimension_1, dimension_2, input_matrix, output_matrix, add=False):
        starting_row1 = dimension_1[0]
        ending_row1 = dimension_1[1]
        starting_col1 = dimension_1[2]
        ending_col1 = dimension_1[3]
        starting_row2 = dimension_2[0]
        ending_row2 = dimension_2[1]
        starting_col2 = dimension_2[2]
        i = 0
        j = 0
        for row in range(starting_row1, ending_row1 + 1):
            for col in range(starting_col1, ending_col1 + 1):
                if not add:
                    output_matrix[i][j] = input_matrix[row][col] - input_matrix[starting_row2][starting_col2]
                else:
                    output_matrix[i][j] = input_matrix[row][col] + input_matrix[starting_row2][starting_col2]
                starting_col2 += 1
                j += 1
            starting_col2 = dimension_2[2]
            j = 0
            starting_row2 += 1
            i += 1


class TestMatrixMultiplication(unittest.TestCase):
    def _test(self, n):
        x = self._build_random_list(n)
        y = self._build_random_list(n)
        print ("X {}".format(x))
        print ("Y {}".format(y))
        matrix1 = Matrix(x)
        matrix2 = Matrix(y)
        result1 = matrix1.divide_conquer_matrix_multiplication(matrix2)
        print("Divide and Conquer Result: {}".format(result1))
        result2 = matrix1 * matrix2
        print("Native Result: {}".format(result2))
        self.assertTrue(result1 == result2)
        if n % 2 == 0:
            result3 = matrix1.straussen_matrix_multiplication(matrix2)
            print("Straussen Result : {}".format(result3))
            self.assertTrue(result2 == result3)

    def test_4x4(self):
        self._test(4)

    def test_2x2(self):
        self._test(2)

    def test_3x3(self):
        self._test(3)

    def test_5x5(self):
        self._test(5)

    def _build_random_list(self, n):
        z = list()
        for i in range(n):
            sublist = list()
            for j in range(n):
                sublist.append(random.randint(1, 9))
            z.append(sublist)
        return z


if __name__ == '__main__':
    unittest.main()












