lint:
	poetry run flake8 .

black:
	poetry run black .

test:
	poetry run pytest