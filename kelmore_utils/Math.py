import math
import datetime


class Maths:

    @staticmethod
    def convert_string_date_to_seconds(date, date_format):
        """
        Converts a date (in string format) to seconds after the epoch
        :param date: The date to be formatted (as a string)
        :param date_format: The format rules for the date (e.g. "%m/%d/%Y)
        :return: The number of seconds since the epoch for the date
        """
        epoch = datetime.datetime.utcfromtimestamp(0)
        return (datetime.datetime.strptime(date, date_format) - epoch).total_seconds()

    @staticmethod
    def fibonacci(num):
        """ precondition:  n is a non-negative  integer
            postcondition:  returns the fibonacci sum of n"""
        return Maths.maserati(num)[1]

    @staticmethod
    def maserati(num):
        """ precondition:  n is a non-negative  integer
            postcondition:  helper method that returns the fibonacci sum of n"""
        if num == 0:
            return [-1, 0]
        if num == 1:
            return [0, 1]
        output = Maths.maserati(num - 1)
        return [output[1], output[0] + output[1]]

    @staticmethod
    def prime_factors(num):
        """ prec: n is an integer
            postc: returns the prime factors of x"""
        if num == 1:
            return []
        smallest_factor = Maths.smallest_factor(num)
        return [smallest_factor] + Maths.prime_factors(int(num) / smallest_factor)

    @staticmethod
    def is_prime(num):
        """ prec: n is an integer
            postc: returns True if x is prime, False otherwise"""
        prime_check = 2
        while prime_check * prime_check <= num:
            if num % prime_check == 0:
                return False
            prime_check += 1
        return True

    @staticmethod
    def positivity(num):
        """ precondition:  num is an integer
            postcondition:  returns 1 if num is positive, 0 for 0, and -1 if negative"""
        if num < 0:
            return -1
        if num > 0:
            return 1
        return 0

    @staticmethod
    def hypotenuse(num_a, num_b):
        """ precondition: a and b are numbers
            postcondition: returns the length of the hypotenuse of a right triangle
                            with legs of length a and b."""
        return (num_a ** 2 + num_b ** 2) ** .5

    @staticmethod
    def third_side(num_a, num_b, theta):
        """ precondition: a, b, and theta are numbers.
                            a and b are the side lengths of a triangle, and theta is an angle in
                            radians.
            postcondition: returns the length of the third side"""
        return math.sqrt(num_a * num_a + num_b * num_b - 2 * num_a * num_b * math.cos(theta))

    @staticmethod
    def mean(num):
        """ precondition:  num is a numerical list
            postcondition:  returns the average of the numbers is num"""
        return sum(num) / float(len(num))

    @staticmethod
    def sum_squares(num):
        """ precondition:  num is a non-negative  integer
            postcondition:  returns the sum of the squares of the integers 0-num"""
        num = range(num + 1)
        num = [k * k for k in num]
        return sum(num)

    @staticmethod
    def bang(num):
        """ precondition:  nn is a non-negative  integer
            postcondition:  returns n!"""
        return 1 if num == 0 else num * Maths.bang(num - 1)

    @staticmethod
    def product(num):
        """ prec: x is a list of numbers
            postc: returns the product of the list"""
        product = 1
        for k in num:
            product *= k
        return product

    @staticmethod
    def is_even(num):
        """ prec: x is an integer
            postc: returns True if x is even, False otherwise"""
        if num == 0:
            return False
        if num % 2 == 0:
            return True
        return False

    @staticmethod
    def smallest_factor(num):
        """ prec: n is an integer
            postc: returns the smallest factor of n"""
        k = 2
        while k * k <= num:
            if num % k == 0:
                return k
            k += 1
        return num

    @staticmethod
    def biggest_sine(list_of_floats):
        """ prec: x is a list of floats.
            postc:  returns the largest sine of the list of floats"""
        floats = list_of_floats
        floats = [math.sin(k) for k in floats]
        floats.sort()
        return floats[-1]

    # Can alternatively use python math for functions below
    @staticmethod
    def absolute_value(num):  # to define f(x), Boss statement (owns indented code)
        """ prec: x is an integer
            postc: returns x if x is positive, -x if x is negative"""
        return num if num >= 0 else -num

    @staticmethod
    def maximum(num):
        """ prec: x is a list of numbers
            postc: returns the largest number in x"""
        num.sort()
        return num[-1]

    @staticmethod
    def minimum(num):
        """ prec: x is a list of numbers
            postc: returns the smallest number in x"""
        num.sort()
        return num[0]

    @staticmethod
    def square(num):
        """ prec: x is an integer
            postc: returns the square of x"""
        return num * num

    @staticmethod
    def cube(num):
        """ prec: x is an integer
            postc: returns the cube of x"""
        return num * num * num

    @staticmethod
    def calculate_standard_deviation(nums):
        """
        Calculates the standard deviation from a list of numbers
        :param nums: A list of numbers
        :return: The standard deviations
        """
        _mean = 0
        for num in nums:
            _mean += num
        _mean = _mean / len(nums)

        _sum = 0.0
        for num in nums:
            _sum += (float(num) - float(_mean)) ** 2

        return (_sum / float(len(nums))) ** 0.5
