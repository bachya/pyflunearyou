clean:
	. .venv/bin/activate; pre-commit uninstall
	rm -rf .venv/
coverage:
	.venv/bin/py.test -s --verbose --cov-report term-missing --cov-report xml --cov=pyflunearyou tests
init:
	virtualenv .venv
	.venv/bin/pip3 install poetry
	. .venv/bin/activate; poetry lock; poetry install; pre-commit install
lint:
	.venv/bin/black --check --fast pyflunearyou
	.venv/bin/flake8 pyflunearyou
	.venv/bin/pydocstyle pyflunearyou
	.venv/bin/pylint pyflunearyou
publish:
	.venv/bin/poetry build
	.venv/bin/poetry publish
	rm -rf dist/ build/ .egg *.egg-info/
test:
	.venv/bin/py.test
typing:
	.venv/bin/mypy --ignore-missing-imports pyflunearyou
