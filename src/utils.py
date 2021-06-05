from typing import Iterable, Union

FloatOrStr = Union[float, str]


def compare_floats_with_epsilon(left: float, right: float, epsilon: float = 10e-12) -> bool:
    return abs(right - left) < epsilon


def compare_with_list_of_floats(left: float, right: Iterable[float], epsilon: float = 10e-12) -> bool:
    result: bool = False
    for elem in right:
        result |= compare_floats_with_epsilon(left, elem, epsilon=epsilon)
        if result:
            break
    return result


def sqrt(num: float, epsilon: float = 10e-12) -> float:
    """
    source: https://stackoverflow.com/a/3047531/8990391
    """
    if compare_floats_with_epsilon(num, 0.0):
        return 0.0
    if num < 0.0:
        raise ValueError("sqrt принимает только положительные значения")
    last_guess = num / 2
    while True:
        guess = (last_guess + num / last_guess) / 2
        if abs(guess - last_guess) < epsilon:
            return guess
        last_guess = guess


def sqr(num: float) -> float:
    """
    I improved the code from https://stackoverflow.com/a/3519308/8990391
    """
    return num * num


def pow(num: float, degree: float, epsilon: float = 10e-12) -> float:
    """
    I improved the code from https://stackoverflow.com/a/3519308/8990391
    """
    sign = 1
    if num < 0.0:
        if int(degree) != degree:
            raise ValueError("Мнимые числа при возведении в степень")
        degree = int(degree)
        if degree % 2 == 1:
            sign = -1
        num = -num
    if compare_floats_with_epsilon(num, 0.0):
        if degree < 0.0:
            raise ZeroDivisionError("Деление на ноль при возведении в степень")
        elif compare_floats_with_epsilon(degree, 0.0):
            return 1
        return 0
    if compare_floats_with_epsilon(degree, 0.0):
        return 1
    if degree < 0:
        return 1 / pow(num, -degree, epsilon)
    if degree >= 10:
        return sign * sqr(pow(num, degree / 2, epsilon / 2))
    if degree >= 1:
        return sign * num * pow(num, degree - 1, epsilon)
    if epsilon >= 1:
        return sign * sqrt(num)
    return sign * sqrt(pow(num, degree * 2, epsilon * 2))


def floor(num: float) -> float:
    return int(num) - (num < 0)
