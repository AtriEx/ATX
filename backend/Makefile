format fmt:
	isort --profile black .
	black .

lint-only:
	pylint *.py **/*.py

lint: format lint-only

check-format:
	isort --profile black --check .
	black --check .

ci: check-format lint-only
