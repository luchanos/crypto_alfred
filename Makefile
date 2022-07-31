flake8-check:
	flake8 --config=.flake8

black-check:
	black . --config pyproject.toml --check

isort-check:
	isort . --diff --check

black:
	black . --config pyproject.toml

isort:
	isort .

linters-check: isort-check black-check flake8-check

linters: isort black flake8-check
