install:
	pip install -r requirements.txt

run:
	flask run

migrate:
	flask db init
	flask db migrate -m "Initial migration."
	flask db upgrade

test:
	pytest --cov=app tests/

.PHONY: install run migrate test
