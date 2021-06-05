The file `en.subject.pdf` describes the task

Tests:
- run `pytest` command in the root directory

Steps:
- `python -m venv myvenv`
- `python -m pip install -r requirements.txt`
- `python compuctor.py "<equation string>"`

The equation can contain only
- the following symbols: `+*/^0-9.=X-`

Bonuses:
You can
- add a sign (`+`/`-`) to a number anywhere in an equation, e.g. `X^+2 - -2 * X^1 + -3 * X^0 = +0.0` 
- compose fractions of all kinds including degrees of X, e.g. `11.11*X^4/X^2*21.23/X^1*12.32`
- raise a number to a power: `2.1^4.3 * X^2`
