clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	rm -rf .pytest_cache htmlcov .coverage .coverage.xml .mypy_cache 2>/dev/null || true

lint:
	uv run flake8 .

black:
	uv run black .

test:
	uv run pytest --cov=src --cov-report=term --cov-report=html tests/ && uv run flake8 . && uv run black --check .

test-coverage:
	uv run pytest --cov=src --cov-report=term --cov-report=html --cov-report=xml tests/
