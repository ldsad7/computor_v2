import click

from src.equation_parser import EquationParser
from src.equation_solver import EquationSolver


@click.command('extra-class calculator')
@click.option("--verbose", is_flag=True, default=False, help="verbose output")
def main(verbose: bool = False):
    if verbose:
        print('Начинаем парсинг уравнения')
    equation_parser: EquationParser = EquationParser(equation, verbose)
    equation_parser.parse_equation()
    if verbose:
        print('Парсинг уравнения успешен')
        print('Начинаем решать уравнение')
    equation_solver: EquationSolver = EquationSolver(equation_parser.multipliers, verbose)
    equation_solver.solve_equation()
    if verbose:
        print('Уравнение успешно решено')


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f'Error happened: {e}')
