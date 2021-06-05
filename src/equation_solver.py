from typing import Dict, Tuple, Any, List

from utils import compare_floats_with_epsilon, sqrt


class EquationSolver:
    def __init__(self, multipliers: Dict[float, float], verbose: bool):
        self.c = multipliers[0]
        self.b = multipliers[1]
        self.a = multipliers[2]
        self.verbose = verbose

    def solve_equation(self) -> List[Any]:
        if not compare_floats_with_epsilon(self.a, 0.0):
            result = self.solve_quadratic_equation()
        elif not compare_floats_with_epsilon(self.b, 0.0):
            result = self.solve_linear_equation()
        else:
            result = self.solve_zero_degree_equation()
        return sorted(result)

    def solve_zero_degree_equation(self) -> Tuple[str]:
        if compare_floats_with_epsilon(self.c, 0.0):
            print('Любое значение X является решением данного уравнения.')
            return 'any',
        else:
            print('У данного уравнения нет решений.')
            return 'no',

    def solve_linear_equation(self) -> Tuple[float]:
        x = -self.c / self.b
        print(f'Уравнение имеет одно решение.\nРешение данного уравнения: X = {x}')
        return x,

    def solve_quadratic_equation(self) -> Tuple[Any, ...]:
        discriminant: float = self.b * self.b - 4 * self.a * self.c
        if compare_floats_with_epsilon(discriminant, 0.0):
            x = -self.b / (2 * self.a)
            if self.verbose:
                print(f'Дискриминант равен нулю')
            print(f'Уравнение имеет 2 совпадающих вещественных решения:\nx0 = {x}\nx1 = {x}')
            return x,
        elif discriminant > 0:
            discriminant_sqrt = sqrt(discriminant)
            x0 = (-self.b + discriminant_sqrt) / (2 * self.a)
            x1 = (-self.b - discriminant_sqrt) / (2 * self.a)
            if self.verbose:
                print(f'Дискриминант больше нуля')
            print(f'Уравнение имеет 2 вещественных решения:\nx0 = {x0}\nx1 = {x1}')
            return x0, x1
        else:
            discriminant_sqrt = sqrt(-discriminant)
            operand1 = -self.b / (2 * self.a)
            if compare_floats_with_epsilon(operand1, 0.0):
                operand1 = abs(operand1)
            operand2 = discriminant_sqrt / (2 * self.a)
            if operand2 > 0.0:
                signs = ['+', '-']
            else:
                operand2 *= -1
                signs = ['-', '+']
            x0 = f'{operand1} {signs[0]} {operand2} * i'
            x1 = f'{operand1} {signs[1]} {operand2} * i'
            if self.verbose:
                print(f'Дискриминант меньше нуля')
            print(f'Уравнение не имеет вещественных решений и имеет 2 мнимых решения:\nx0 = {x0}\nx1 = {x1}')
            return x0, x1

