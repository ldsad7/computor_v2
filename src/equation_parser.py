import re
from collections import defaultdict
from typing import Tuple, List, DefaultDict

from utils import compare_floats_with_epsilon, pow, FloatOrStr


class EquationParser:
    def __init__(self, equation: str, verbose: bool) -> None:
        self.equation = re.sub(r'\s+', '', equation)
        self.multipliers: DefaultDict[float, float] = defaultdict(float)
        self.verbose = verbose

    @staticmethod
    def replace_one_value(value: float) -> str:
        if compare_floats_with_epsilon(value, 1.0):
            return ''
        return f'{value}*'

    def check_verbose(self) -> None:
        if self.verbose:
            degree_two = not compare_floats_with_epsilon(self.multipliers[2.0], 0.0)
            degree_one = not compare_floats_with_epsilon(self.multipliers[1.0], 0.0)
            degree_zero = not compare_floats_with_epsilon(self.multipliers[0.0], 0.0)
            degree = 0
            if degree_two:
                degree = 2
            elif degree_one:
                degree = 1
            equation = ''
            need_sign = False
            if degree_two:
                if self.multipliers[2.0] < 0.0:
                    for key, value in self.multipliers.items():
                        self.multipliers[key] = -value
                equation += f'{self.replace_one_value(self.multipliers[2.0])}X^2 '
                need_sign = True
            if degree_one:
                if not need_sign:
                    if self.multipliers[1.0] < 0.0:
                        for key, value in self.multipliers.items():
                            self.multipliers[key] = -value
                    equation += f'{self.replace_one_value(self.multipliers[1.0])}X '
                    need_sign = True
                else:
                    if self.multipliers[1.0] < 0.0:
                        equation += f'- {self.replace_one_value(-self.multipliers[1.0])}X '
                    else:
                        equation += f'+ {self.replace_one_value(self.multipliers[1.0])}X '
            if degree_zero:
                if not need_sign:
                    if self.multipliers[0.0] < 0.0:
                        for key, value in self.multipliers.items():
                            self.multipliers[key] = -value
                    equation += f'{self.multipliers[0.0]} '
                else:
                    if self.multipliers[0.0] < 0.0:
                        equation += f'- {-self.multipliers[0.0]} '
                    else:
                        equation += f'+ {self.multipliers[0.0]} '
            if not equation:
                equation += '0.0 '
            equation += '= 0.0'
            print(f'Степень уравнения: {degree}')
            print(f'Сокращённая форма: {equation}')

    def parse_equation(self) -> None:
        if not re.fullmatch('[+*/^0-9.=X-]*', self.equation):
            raise ValueError("Уравнение некорректно (в уравнении есть недопустимый символ)")
        parts = self.equation.split('=')
        if len(parts) != 2:
            raise ValueError("Уравнение некорректно (либо нет знака '=', либо больше 1)")
        for i, part in enumerate(parts):
            self.parse_part(part, 1 - 2 * i)
        to_delete = []
        for key, value in self.multipliers.items():
            if key not in range(3) and compare_floats_with_epsilon(value, 0.0):
                to_delete.append(key)
        for key in to_delete:
            del self.multipliers[key]
        if set(self.multipliers.keys()) - set(range(3)):
            raise ValueError('Уравнение некорректно (есть компонент с некорректной степенью либо меньше 0, '
                             'либо больше 2, либо нецелой)')
        self.check_verbose()

    def parse_part(self, part: str, sign: int) -> None:
        compounds = re.sub(r'([^+*^/-])(\+)', r'\1|', part).split('|')
        if len(compounds) > 1:
            for compound in compounds:
                self.parse_part(compound, sign)
            return
        compounds = re.sub(r'([^+*^/-])(-)', r'\1|', part).split('|')
        if len(compounds) > 1:
            self.parse_part(compounds[0], sign)
            for compound in compounds[1:]:
                self.parse_part(compound, sign * -1)
            return
        self.parse_compound(part, sign)

    def parse_compound(self, compound: str, sign: int):
        fractions = compound.split('*')
        nominators = []
        denominators = []
        for fraction in fractions:
            nominator, literal_denominators = self.parse_fraction(fraction)
            nominators.append(nominator)
            denominators.extend(literal_denominators)
        multiplier, degree = self.check_fraction(nominators, denominators)
        self.multipliers[degree] += multiplier * sign

    def parse_fraction(self, fraction: str) -> Tuple[FloatOrStr, List[FloatOrStr]]:
        operands = fraction.split('/')
        nominator = self.parse_operand(operands[0])
        denominators = [self.parse_operand(operand) for operand in operands[1:]]
        return nominator, denominators

    def parse_operand(self, operand: str) -> FloatOrStr:
        literals = operand.split('^', 1)
        if len(literals) == 1:
            if literals[0] == 'X':
                return f'{literals[0]}^1'
            return self.parse_number(literals[0])
        power = self.parse_operand(literals[1])
        if isinstance(power, str):
            raise ValueError("X не может быть в степени, X может быть только возводиться в степень")
        if literals[0] == 'X':
            return f'{literals[0]}^{power}'
        return pow(self.parse_number(literals[0]), power)

    @staticmethod
    def parse_number(literal: str) -> float:
        if not re.fullmatch(r'[+-]?\d+(\.\d+)?', literal):
            raise ValueError(f"Уравнение некорректно (некорректный литерал {literal})")
        if not literal:
            raise ValueError("Уравнение некорректно (пропущено слагаемое)")
        try:
            value = float(literal)
        except ValueError:
            raise ValueError(f"Уравнение некорректно (некорректный литерал {literal})")
        return value

    def check_fraction(self, nominators: List[FloatOrStr], denominators: List[FloatOrStr]) -> Tuple[float, float]:
        nominator_multiplier, nominator_degree = self.get_multiplier_and_degree(nominators)
        denominator_multiplier, denominator_degree = self.get_multiplier_and_degree(denominators)
        if compare_floats_with_epsilon(denominator_multiplier, 0.0):
            raise ZeroDivisionError('Уравнение некорректно (есть деление на 0)')
        multiplier = nominator_multiplier / denominator_multiplier
        degree = nominator_degree - denominator_degree
        return multiplier, degree

    @staticmethod
    def get_multiplier_and_degree(values: List[FloatOrStr]) -> Tuple[float, float]:
        multiplier = 1.0
        degree = 0.0
        for value in values:
            if isinstance(value, float):
                multiplier *= float(value)
            else:
                degree += float(value[2:])
        return multiplier, degree

    def __str__(self):
        string = f'{self.multipliers[2]}*X^2 '
        if self.multipliers[1] < 0.0:
            string += f'- {-self.multipliers[1]}*X^1 '
        else:
            string += f'+ {self.multipliers[1]}*X^1 '
        if self.multipliers[0] < 0.0:
            string += f'- {-self.multipliers[0]}'
        else:
            string += f'+ {self.multipliers[0]}'
        string += ' = 0.0'
        return string
