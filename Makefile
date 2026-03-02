clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	rm -rf .pytest_cache htmlcov .coverage .coverage.xml .mypy_cache 2>/dev/null || true

lint:
	poetry run flake8 .

black:
	poetry run black .

test:
	poetry run pytest --cov=src --cov-report=term --cov-report=html tests/ && poetry run flake8 --extend-ignore=E203,W503,E704,S104,S101,SIM910,SIM117,D100,D101,D102,D103,D400,D401,I100,I201,Q000,E501,BLK100 . && poetry run black --check .

test-coverage:
	poetry run pytest --cov=src --cov-report=term --cov-report=html --cov-report=xml tests/
