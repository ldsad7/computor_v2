from typing import Dict, Tuple, Any

import pytest

from equation_parser import EquationParser
from equation_solver import EquationSolver
from utils import compare_floats_with_epsilon, sqrt, pow, compare_with_list_of_floats


class TestParser:
    @staticmethod
    def check_equation(equation: str, correct_multipliers: Dict[float, float]):
        parser: EquationParser = EquationParser(equation, False)
        parser.parse_equation()
        equation_multipliers = parser.multipliers
        for i in range(3):
            assert compare_floats_with_epsilon(correct_multipliers[i], equation_multipliers[i])

    @staticmethod
    def check_equation_raises_error(equation: str, error_type):
        parser: EquationParser = EquationParser(equation, False)
        with pytest.raises(error_type):
            parser.parse_equation()

    @staticmethod
    def check_equation_raises_zero_division_error(equation: str):
        TestParser.check_equation_raises_error(equation, ZeroDivisionError)

    @staticmethod
    def check_equation_raises_value_error(equation: str):
        TestParser.check_equation_raises_error(equation, ValueError)

    def test_correct_equations(self):
        equations = [
            ["0=0", {0: 0, 1: 0, 2: 0}],
            ["X^2= 0", {0: 0, 1: 0, 2: 1}],
            ["X^1 =0", {0: 0, 1: 1, 2: 0}],
            ["X^2 + X^1 = 0", {0: 0, 1: 1, 2: 1}],
            ["X^2 + X^1 + X^0=0", {0: 1, 1: 1, 2: 1}],
            ["2.5 * X^2 + 3/ 2*X^1 + 4/ 2 /2 * 10*X^0= 0",
             {0: 10, 1: 1.5, 2: 2.5}],
            ["-3.5 *X^2-2.1*X^2 - 1.4*X^1 -7 /2*X^0   +  X^0 +21.0*X^2=0",
             {0: -2.5, 1: -1.4, 2: 15.4}],
            ["-7 /2*X^0 +-3.5 *X^2 - 1.4*X^1   +  X^0 -2.1*X^2 +21.0*X^2= -23.3*X^1+ 13.4*X^2 + 0.2 *X^0",
             {0: -2.7, 1: 21.9, 2: 2}],
            ["2*2.3*1/0.5/2*3/4*X^2=1/2*2/2/4*4*X^2/2/X^2",
             {0: -0.25, 1: 0.0, 2: 3.45}],
            ["-2.000/+20000.3*+1/-0.5/-2*3/4/0.4*X^3/X^1*2.0 - -2*X^0*X^2*X^1/X^2*-2.0334*X^0/X^0 + + 31.4*X^4/X^3*2 -"
             " +12*X^2/X^2=0.0000",
             {0: -12.0, 1: 58.7332, 2: -0.0003749943750843737343939840902}],
            ["X^+100 / X^99 = 1",
             {0: -1.0, 1: 1.0, 2: 0.0}],
            ["X^-100 / X^-101 = 4",
             {0: -4.0, 1: 1.0, 2: 0.0}],
            ["X^2 + X^1^100.32^3.12 + X^0=0",
             {0: 1, 1: 1, 2: 1}],
            ["X^-2.0^+1.0000*X^4 + X^1^100.32^3.12 + X^0=0",
             {0: 1, 1: 1, 2: 1}],
            ["X^-2.0^-2.0000*X^1.75 + X^1^100.32^3.12 + X^0=0",
             {0: 1, 1: 1, 2: 1}],
            ["X^2^1^1^3^6 + X^-100.1^0.0 + X^0=0",
             {0: 1, 1: 1, 2: 1}],
            ["X^2^1^1^3^6 + X^0^0.0 + X^0=0",
             {0: 1, 1: 1, 2: 1}],
            ["-2*X + X*X + X^0=0",
             {0: 1, 1: -2, 2: 1}]
        ]
        for equation_group in equations:
            equation, equation_multipliers = equation_group
            self.check_equation(equation, equation_multipliers)

    def test_error_equations(self):
        equations_value_error = [
            "0",
            "0=",
            "0 = 0 = 0",
            "X^0 + X^2",
            "X^2 = X^^2",
            "X^--2 = 0",
            "Y^2-1=0",
            "X^2 + X^1 - X^0 + 10e5 = 0",
            "++0 = 0",
            "X^3 = 0",
            "X^100 / X^97 = 0",
            "X^97 / X^100 - 3 = 0",
            "X^97 / X^(100 - 3) = 0",
            "X^1 * X^2 = 0",
            "X+^1 = 0",
            "- = 0",
            "+ = 0",
            "",
            "=",
            "=1",
            "1=1 + X^4",
            "X^-100 / X^-99 = 4",
            "X.0 = 1.0",
            "X^.0 = 1.0",
            "X^3 * X^1.4 = 1.0",
            "X^1.5 = 1.0",
            "X_1 = 1.0",
            "X^^ = 23.10",
            "X^1^ - 2 * X^2 = 0",
            "X^2^2 + X^1 + X^0=0",
            "X^X^2 = 0",
            "X^2^X^4 = 0",
            "2^3^X^2 = 0",
            "2^3^-4.01^X=0",
            "XX = 0",
            "X^9=0 - X = 0",
            "X^9^ = 0",
            "X^-2.2^-3.3 = 0"
        ]
        for equation in equations_value_error:
            self.check_equation_raises_value_error(equation)
        equations_zero_division_error = [
            "X^0^-3.3 = 0"
        ]
        for equation in equations_zero_division_error:
            self.check_equation_raises_zero_division_error(equation)


class TestSolver:
    @staticmethod
    def check_solution(coefs: Dict[float, float], expected_result: Tuple[Any, ...]):
        equation_solver: EquationSolver = EquationSolver(coefs, False)
        actual_result = equation_solver.solve_equation()
        assert len(actual_result) == len(actual_result)
        for expected_elem, actual_elem in zip(expected_result, actual_result):
            assert type(expected_elem) == type(actual_elem)
            if isinstance(expected_elem, float):
                assert compare_floats_with_epsilon(expected_elem, actual_elem)
            else:
                assert expected_elem == actual_elem

    def test_zero_degree_equation(self):
        tests = [
            [{0: 32.1, 1: 0.0, 2: 0.0}, ('no',)],
            [{0: 0.0, 1: 0.0, 2: 0.0}, ('any',)],
            [{0: 0.00000000000000000000000000001, 1: 0.0,
              2: 0.0}, ('any',)],
            [{0: -0.00000000000000000000000000001, 1: 0.0,
              2: 0.0}, ('any',)],
            [{0: -0.000001, 1: 0.0,
              2: 0.0}, ('no',)],
            [{0: 0.000001, 1: 0.0, 2: 0.0}, ('no',)]
        ]
        for coefs, result in tests:
            self.check_solution(coefs, result)

    def test_linear_equation(self):
        tests = [
            [{0: 32.1, 1: 2.3, 2: 0.0},
             (-32.1 / 2.3,)],
            [{0: 2.3, 1: -32.1, 2: 0.0},
             (2.3 / 32.1,)],
            [{0: -3.4, 1: -5.6, 2: 0.0},
             (-3.4 / 5.6,)],
            [{0: -64.1, 1: 2.4, 2: 0.0},
             (64.1 / 2.4,)]
        ]
        for coefs, result in tests:
            self.check_solution(coefs, result)

    def test_quadratic_equation(self):
        tests_discriminant_zero = [
            [{0: 9.0, 1: -6.0, 2: 1.0}, (3.0, 3.0)],
            [{0: -23.12, 1: -13.6, 2: -2.0}, (-3.4, -3.4)],
            [{0: 0.0, 1: 0.0, 2: 112.0}, (0.0, 0.0)]
        ]
        tests_discriminant_positive = [
            [{0: -3.2, 1: 0.0, 2: 4.6}, (-0.8340576562282990507125979239, 0.8340576562282990507125979239)],
            [{0: 3.2, 1: 0.0, 2: -4.6}, (-0.8340576562282990507125979239, 0.8340576562282990507125979239)],
            [{0: -6.0, 1: 1.0, 2: 1.0}, (-3.0, 2.0)],
            [{0: 31.442578357, 1: 23.2377135, 2: 4.1}, (-3.435435000010138, -2.2322999999898627)],  # overflow
            [{0: 0.0, 1: -11.25, 2: 3.0}, (0.0, 3.75)],
            [{0: 0.0, 1: -11.25, 2: 3.0}, (0.0, 3.75)],
            [{0: -16.0, 1: -4.0, 2: 2.0}, (-2.0, 4.0)]
        ]
        tests_discriminant_negative = [
            [{0: 4.0, 1: 0.0, 2: 1.0}, ('0.0 + 2.0 * i', '0.0 - 2.0 * i')],
            [{0: -27.3, 1: 8.4, 2: -2.1}, ('2.0 + 3.0 * i', '2.0 - 3.0 * i')],
            [{0: 4.42, 1: -4.2, 2: 1}, ('2.1 + 0.09999999999999894 * i', '2.1 - 0.09999999999999894 * i')]
        ]
        for tests in [tests_discriminant_zero, tests_discriminant_positive, tests_discriminant_negative]:
            for coefs, result in tests:
                self.check_solution(coefs, result)


class TestUtils:
    def test_sqrt(self):
        test_sets = [
            [0.0, 0.0],
            [0.25, 0.5],
            [1.0, 1.0],
            [100.0, 10.0],
            [315.2354235, 17.754870416311128],
            [10 ** 10, 10 ** 5]
        ]
        error_values = [-0.25, -0.001, -123.5325, -645634.43]

        for arg, expected_result in test_sets:
            assert compare_floats_with_epsilon(sqrt(arg), expected_result)
        for error_value in error_values:
            with pytest.raises(ValueError):
                sqrt(error_value)

    def test_pow(self):
        test_sets = [
            [4.0, 0.5, 2.0],
            [4.0, -0.5, 0.5],
            [4.0, 0.0, 1.0],
            [4.0, 1.0, 4.0],
            [10 ** 5, 1.0, 10 ** 5],
            [0.0, 0.0, 1.0],
            [-2.12, 0.0, 1.0],
            [-2.12, 2.0, 4.4944],
            [-2.12, 3.0, -9.528128],
            [-1.0, 4.0, 1.0],
            [-1.0, 5.0, -1.0]
        ]
        value_error_values = [
            [-4.0, 2.5],
            [-4.0, -2.0001],
            [-352.214, -2.5],
            [-416.35, -2.0001]
        ]
        zero_division_error_values = [
            [0.0, -1],
            [10e-15, -4],
            [0.0, -1231241],
            [0.0, -0.000001]
        ]

        for num, degree, expected_result in test_sets:
            assert compare_floats_with_epsilon(pow(num, degree), expected_result)
        for num, degree in value_error_values:
            with pytest.raises(ValueError):
                print(num, degree)
                pow(num, degree)
        for num, degree in zero_division_error_values:
            with pytest.raises(ZeroDivisionError):
                pow(num, degree)

    def test_compare_with_list_of_floats(self):
        tests = [
            [10.0, [123.35235, 10.0000000001, -15235.1], False],
            [10.0, [123.35235, 10.00000000000000000000001, -15235.1], True]
        ]
        for left, right, result in tests:
            assert compare_with_list_of_floats(left, right) is result
