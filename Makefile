start:
	poetry run uvicorn "books:app" --reload

run_e2e:
	poetry run e2e

run_integration:
	poetry run integration

tests: run_e2e run_integration
