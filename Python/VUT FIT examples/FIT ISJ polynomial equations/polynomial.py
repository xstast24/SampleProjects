#!/usr/bin/env python3


# ISJ project 2
# Filip Stastny
# xstast24


class Polynomial:
    def __init__(self, *args, **kwargs):
        """
        Init polynomial object from integers symbolizing polynomial coeficients.
        Example: Polynomial(-1, 0, 1, 2) creates a representation of polynomial '2x^3 + x^2 - 1'.
        :param list: list of integers, eg. [1, 0, -2]
        :param positional integers: tuple of integers, eg. 1, 2, 0, 2
        :param key-value integers: indexed integers, eg. x1=1, x3=-2, x5=1
        """
        # valid params check
        if len(args) == 1 and type(args[0]) != int and type(args[0]) != list:
            raise Exception("Polynomial can be created only from integers.")
        elif len(args) > 1:
            for arg in args:
                if type(arg) != int:
                    raise Exception("Polynomial can be created only from integers.")

        if len(kwargs) > 0:
            for arg in kwargs.values():
                if type(arg) != int:
                    raise Exception("Polynomial can be created only from integers.")

        # get params
        if len(args) == 1 and len(kwargs) == 0 and type(args[0]) == list:
            self.polynom = args[0]
        elif len(args) > 0 and len(kwargs) == 0:
            self.polynom = []
            for x in args:
                self.polynom.append(x)
        elif len(kwargs) > 0 and len(args) == 0:
            self.polynom = []
            cnt = 0
            i = 0
            while len(kwargs) > cnt:
                if 'x{0}'.format(i) in kwargs.keys():
                    cnt += 1
                    self.polynom.append(kwargs['x{0}'.format(i)])
                else:
                    self.polynom.append(0)
                i += 1
        else:
            raise Exception("Wrong usage of polynomial class.")

    def __str__(self):
        """
        Return string representation of polynomial instance, eg. (-1, 0, 1, 2) return a polynomial (2x^3 + x^2 - 1).
        """
        result = ""
        exponent = len(self.polynom)
        for number in reversed(self.polynom):
            exponent -= 1
            if number != 0:  # number is not zero > add it to result string
                if exponent == 0:
                    if result == "":
                        if number > 0:
                            result = str(number)
                        elif number < 0:
                            result = '- ' + str(abs(number))
                    else:
                        if number > 0:
                            result = result + ' + ' + str(number)
                        elif number < 0:
                            result = result + ' - ' + str(abs(number))
                elif exponent == 1:
                    if result == "":  # first/highest polynomial member
                        if number == 1:
                            result = 'x'
                        elif number > 1:
                            result = str(number) + 'x'
                        elif number == -1:
                            result = '- x'
                        elif number < 0:
                            result = '- ' + str(abs(number)) + 'x'
                    else:  # other polynomial member
                        if number == 1:
                            result += ' + x'
                        elif number > 1:
                            result = result + ' + ' + str(number) + 'x'
                        elif number == -1:
                            result += ' - x'
                        elif number < 0:
                            result = result + ' - ' + str(abs(number)) + 'x'
                else:
                    if result == "":  # first/highest polynomial member
                        if number == 1:
                            result = 'x^' + str(exponent)
                        elif number > 1:
                            result = str(number) + 'x^' + str(exponent)
                        elif number == -1:
                            result = '- x^' + str(exponent)
                        elif number < 0:
                            result = '- ' + str(abs(number)) + 'x^' + str(exponent)
                    else:  # other polynomial member
                        if number == 1:
                            result = result + ' + x^' + str(exponent)
                        elif number > 1:
                            result = result + ' + ' + str(number) + 'x^' + str(exponent)
                        elif number == -1:
                            result = result + ' - x^' + str(exponent)
                        elif number < 0:
                            result = result + ' - ' + str(abs(number)) + 'x^' + str(exponent)
        if result == "":
            return "0"
        else:
            return str(result)

    def __add__(self, other):
        """
        Adding of two polynomials, returns a new Polynomial instance.
        """
        # check valid parameter
        if not isinstance(other, Polynomial):
            raise Exception("Only allowed adding polynomial object to another polynomial object.")

        tmp_pol1 = list(self.polynom)
        tmp_pol2 = list(other.polynom)
        length1 = len(tmp_pol1)
        length2 = len(tmp_pol2)
        i = 0
        # make the both polynoms the same length by adding zeroes
        if length1 > length2:
            length = length1
            while i < (length1 - length2):
                tmp_pol2.append(0)
                i += 1
        else:
            length = length2
            while i < (length2 - length1):
                tmp_pol1.append(0)
                i += 1

        sum_pol = []
        i = 0
        while i < length:  # count all members in range of the longer polynom
            sum_pol.append(tmp_pol1[i] + tmp_pol2[i])
            i += 1

        return Polynomial(sum_pol)

    # noinspection PyUnusedLocal
    def __pow__(self, power, modulo=None):
        """
        Polynomial exponencial. Return a new instance of Polynomial class.
        :param power: exponent, eg. 3 for polynomial^3
        """
        if type(power) != int:
            raise Exception("'power' method can be used only with non negative integers.")

        if power == 0:
            return 1
        elif power > 0:
            result = list(self.polynom)
            max_power = (len(self.polynom)-1) * power
            while len(result) <= max_power:
                result.append(0)

            iter_count = 1
            while iter_count < power:
                iter_count += 1
                tmp_result = list(result)
                for index, coef in enumerate(result):  # tmp polynom value reset
                    result[index] = 0

                for index1, coeff1 in enumerate(self.polynom):
                    for index2, coeff2 in enumerate(tmp_result):
                        if coeff2 != 0:
                            result[index1 + index2] += coeff1 * coeff2
        else:
            raise Exception("'power' method can be used only with non negative integers.")

        return Polynomial(result)

    def __eq__(self, other):
        """
        Simple polynomial equality. Convert polynomials to string and compare them.
        """
        if self.__str__() == other.__str__():
            return True
        else:
            return False

    def derivative(self):
        """
        Derivation of polynomial. Returns a new instance of polynomial class.
        """
        # derivated constant is 0
        if len(self.polynom) == 1:
            tmp_pol = [0]
            return Polynomial(tmp_pol)

        tmp_pol = list(self.polynom)
        del tmp_pol[0]
        exponent = 0
        for x in tmp_pol:
            if exponent == 0:
                tmp_pol[exponent] = x
            else:
                tmp_pol[exponent] *= exponent + 1
            exponent += 1

        return Polynomial(tmp_pol)

    def at_value(self, *args):
        """
        Express the polynomial value for the given number. Return an integer.
        Or express the polynomial value for given 2 numbers and returns the result of substracting its values.
        :param args: number or two numbers to express the polynomial value/values
        """
        # check valid args
        if len(args) == 1 or len(args) == 2:
            for arg in args:
                if type(arg) != int and type(arg) != float:
                    raise Exception("'at_value' method can be used only with numbers.")

        i = 0
        result = 0
        if len(args) == 1:
            x = args[0]
            for coeficient in self.polynom:  # iterative sum up at values
                result += coeficient * (x**i)
                i += 1
        elif len(args) == 2:
            x1 = args[0]
            x2 = args[1]
            result1 = 0
            result2 = 0
            for coeficient in self.polynom:
                result1 += coeficient * (x1**i)
                result2 += coeficient * (x2**i)
                i += 1

            result = result2 - result1
        else:
            raise Exception("Too many arguments for method at_value().")

        return result


def test():
    assert str(Polynomial(0,1,0,-1,4,-2,0,1,3,0)) == "3x^8 + x^7 - 2x^5 + 4x^4 - x^3 + x"
    assert str(Polynomial([-5,1,0,-1,4,-2,0,1,3,0])) == "3x^8 + x^7 - 2x^5 + 4x^4 - x^3 + x - 5"
    assert str(Polynomial(x7=1, x4=4, x8=3, x9=0, x0=0, x5=-2, x3= -1, x1=1)) == "3x^8 + x^7 - 2x^5 + 4x^4 - x^3 + x"
    assert str(Polynomial(x2=0)) == "0"
    assert str(Polynomial(x0=0)) == "0"
    assert Polynomial(x0=2, x1=0, x3=0, x2=3) == Polynomial(2,0,3)
    assert Polynomial(x2=0) == Polynomial(x0=0)
    assert str(Polynomial(x0=1)+Polynomial(x1=1)) == "x + 1"
    assert str(Polynomial([-1,1,1,0])+Polynomial(1,-1,1)) == "2x^2"
    pol1 = Polynomial(x2=3, x0=1)
    pol2 = Polynomial(x1=1, x3=0)
    assert str(pol1+pol2) == "3x^2 + x + 1"
    assert str(pol1+pol2) == "3x^2 + x + 1"
    assert str(Polynomial(x0=-1,x1=1)**1) == "x - 1"
    assert str(Polynomial(x0=-1,x1=1)**2) == "x^2 - 2x + 1"
    pol3 = Polynomial(x0=-1,x1=1)
    assert str(pol3**4) == "x^4 - 4x^3 + 6x^2 - 4x + 1"
    assert str(pol3**4) == "x^4 - 4x^3 + 6x^2 - 4x + 1"
    assert str(Polynomial(x0=2).derivative()) == "0"
    assert str(Polynomial(x3=2,x1=3,x0=2).derivative()) == "6x^2 + 3"
    assert str(Polynomial(x3=2,x1=3,x0=2).derivative().derivative()) == "12x"
    pol4 = Polynomial(x3=2,x1=3,x0=2)
    assert str(pol4.derivative()) == "6x^2 + 3"
    assert str(pol4.derivative()) == "6x^2 + 3"
    assert Polynomial(-2,3,4,-5).at_value(0) == -2
    assert Polynomial(x2=3, x0=-1, x1=-2).at_value(3) == 20
    assert Polynomial(x2=3, x0=-1, x1=-2).at_value(3,5) == 44
    pol5 = Polynomial([1,0,-2])
    assert pol5.at_value(-2.4) == -10.52
    assert pol5.at_value(-2.4) == -10.52
    assert pol5.at_value(-1,3.6) == -23.92
    assert pol5.at_value(-1,3.6) == -23.92

if __name__ == '__main__':
    test()