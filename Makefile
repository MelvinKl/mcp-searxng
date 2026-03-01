lint:
	poetry run flake8 .

black:
	poetry run black .

test:
	poetry run pytest --cov=src --cov-report=term --cov-report=html tests/ && poetry run flake8 . && poetry run black --check .

test-coverage:
	poetry run pytest --cov=src --cov-report=term --cov-report=html --cov-report=xml tests/