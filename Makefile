clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	rm -rf .pytest_cache htmlcov .coverage .coverage.xml .mypy_cache 2>/dev/null || true

lint:
	poetry run flake8 .

black:
	poetry run black .

test:
	poetry run pytest --cov=src --cov-report=term --cov-report=html tests/ && poetry run flake8 . && poetry run black --check .

test-coverage:
	poetry run pytest --cov=src --cov-report=term --cov-report=html --cov-report=xml tests/