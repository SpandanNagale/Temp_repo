dev:
	docker compose up -d db && uvicorn app.main:app --port 8080 --reload

test:
	pytest -q tests
