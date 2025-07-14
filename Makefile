# Define a variable for OS-specific environment variable setting
ifeq ($(OS),Windows_NT)
    SET_ENV := set
else
    SET_ENV := export
endif

run:
	$(SET_ENV) FLASK_APP=app/api.py:app && $(SET_ENV) FLASK_ENV=development && python -m flask run

test:
	pytest tests/ -n 4 -sv --log-cli-level=INFO
