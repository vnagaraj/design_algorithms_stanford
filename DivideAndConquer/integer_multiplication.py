__author__ = 'VGN'
import random
import unittest


class IntegerMultiplication:

    def __init__(self, integer):
        self.integer = integer

    def __mul__(self, other):
        return self._brute_force(self.integer, other.integer)

    def karatsuba_multiplication(self, other):
        return self._divide_conquer(self.integer, other.integer)

    def _pad_zero(self,  count):
        padded_zeros = ""
        for i in range(count):
            padded_zeros += "0"
        return padded_zeros


    def _divide_conquer(self, first, second):
        first_str = str(first)
        second_str = str(second)
        padded_zeros =None
        if len(first_str) == 1 or len(second_str) == 1:
            return self._brute_force(first, second)
        if len(first_str) > len(second_str):
            padded_zeros = self._pad_zero(len(first_str)- len(second_str))
            second_str += padded_zeros
        elif len(second_str) > len(first_str):
            padded_zeros = self._pad_zero(len(second_str)- len(first_str))
            first_str += padded_zeros
        if len(first_str) % 2 != 0:
            middle = len(first_str)/2 + 1
        else:
            middle = len(first_str)/2
        a = first_str[0:middle]
        b = first_str[middle:]
        c = second_str[0:middle]
        d = second_str[middle:]
        ac = self._divide_conquer(int(a), int(c))
        bd = self._divide_conquer(int(b), int(d))
        a_sum_b = int(a) + int(b)
        c_sum_d = int(c) + int(d)
        prod = self._divide_conquer(a_sum_b, c_sum_d)
        step4 = prod - bd - ac
        n = len(first_str)
        m = len(second_str)
        factor = pow(10,n/2) * pow(10, m/2)
        step4 = step4 * pow(10, n/2)
        ac = ac * factor
        val = ac + bd + step4
        if padded_zeros:
            str_val = str(val)
            str_val = str_val[:-len(padded_zeros)]
            return int(str_val)
        return val


    def _brute_force(self, first, second):
        tot_prod = 0
        retained_prod = None
        carry_over_prod = 0
        first_str = str(first)
        second_str = str(second)
        factor = 0
        for i in range(len(second_str)-1, -1, -1):
            for j in range(len(first_str)-1, -1, -1):
                 int_prod = int(second_str[i]) * int(first_str[j])
                 int_prod += int(carry_over_prod)
                 if j == 0: # last iteration
                     if retained_prod is not None:
                        retained_prod = str(int_prod) + retained_prod
                     else:
                         retained_prod = str(int_prod)
                 elif retained_prod is not None:
                    retained_prod = str(int_prod)[-1] + retained_prod
                 else:
                    retained_prod = str(int_prod)[-1]
                 if len(str(int_prod)) > 1:
                    carry_over_prod = str(int_prod)[0]
            #if carry_over_prod != 0:
            #   retained_prod  = carry_over_prod + retained_prod
            tot_prod += int(retained_prod) * pow(10,factor)
            factor += 1
            retained_prod = None
            carry_over_prod = 0
        return tot_prod


class TestIntegerMultiplication(unittest.TestCase):

    def test(self):
        (x, y) = self._generate_random_nos()
        print ("X {}".format(x))
        print ("Y {}".format(y))
        a = IntegerMultiplication(x)
        b = IntegerMultiplication(y)
        result1 = x * y
        print("Brute force Result: {}".format(result1))
        result2 = a.karatsuba_multiplication(b)
        print("Karatsuba Result: {}".format(result2))
        self.assertTrue(result1 == result2)

    def _generate_random_nos(self):
        m = random.randint(1, 1000000)
        n = random.randint(1, 1000000)
        return (m, n)


if __name__ == '__main__':
    unittest.main()

