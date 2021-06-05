from src.types.rational_number import RationalNumber
from src.utils import pow, sqrt, floor


class ComplexNumber:
    def __init__(self, real: float, imaginary: float):
        self.real: float = real
        self.imaginary: float = imaginary

    def __add__(self, other):
        if isinstance(other, ComplexNumber):
            return ComplexNumber(self.real + other.real, self.imaginary + other.imaginary)
        elif isinstance(other, RationalNumber):
            return ComplexNumber(self.real + other.number, self.imaginary)

    def __sub__(self, other):
        if isinstance(other, ComplexNumber):
            return ComplexNumber(self.real - other.real, self.imaginary - other.imaginary)
        elif isinstance(other, RationalNumber):
            return ComplexNumber(self.real - other.number, self.imaginary)

    def __mul__(self, other):
        if isinstance(other, ComplexNumber):
            return ComplexNumber(
                self.real * other.real - self.imaginary * other.imaginary,
                self.real * other.imaginary + other.real * self.imaginary
            )
        elif isinstance(other, RationalNumber):
            return ComplexNumber(self.real * other.number, self.imaginary * other.number)

    def __truediv__(self, other):
        if isinstance(other, ComplexNumber):
            denominator: float = self.real * self.real + self.imaginary * self.imaginary
            if denominator == 0:
                raise ZeroDivisionError("an attempt to divide by zero...")
            return ComplexNumber(
                (self.real * other.real + self.imaginary * other.imaginary) / denominator,
                (other.real * self.imaginary - self.real * other.imaginary) / denominator
            )
        elif isinstance(other, RationalNumber):
            if other.number == 0:
                raise ZeroDivisionError("an attempt to divide by zero...")
            return ComplexNumber(self.real / other.number, self.imaginary / other.number)

    def __mod__(self, other):
        if isinstance(other, ComplexNumber):
            if other.modulus == 0:
                raise ZeroDivisionError("an attempt to divide by zero...")
            division_result: ComplexNumber = self / other
            division_result: ComplexNumber = ComplexNumber(
                floor(division_result.real),
                floor(division_result.imaginary)
            )
            return self - other * division_result

    def __pow__(self, other, modulo=None):
        if isinstance(other, ComplexNumber):
            return pow(self.number, other.number)

    @property
    def modulus(self) -> float:
        return sqrt(self.real * self.real + self.imaginary * self.imaginary)
