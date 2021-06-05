from src.utils import pow


class RationalNumber:
    def __init__(self, number: float):
        self.number: float = number

    def __add__(self, other):
        if isinstance(other, RationalNumber):
            return RationalNumber(self.number + other.number)

    def __sub__(self, other):
        if isinstance(other, RationalNumber):
            return RationalNumber(self.number - other.number)

    def __mul__(self, other):
        if isinstance(other, RationalNumber):
            return RationalNumber(self.number * other.number)

    def __truediv__(self, other):
        if isinstance(other, RationalNumber):
            if other.number == 0:
                raise ZeroDivisionError("an attempt to divide by zero...")
            return RationalNumber(self.number / other.number)

    def __mod__(self, other):
        if isinstance(other, RationalNumber):
            if other.number == 0:
                raise ZeroDivisionError("an attempt to divide by zero...")
            return RationalNumber(self.number % other.number)

    def __pow__(self, other, modulo=None):
        if isinstance(other, RationalNumber):
            return pow(self.number, other.number)
