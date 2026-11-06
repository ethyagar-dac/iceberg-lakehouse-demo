# Every target is a command, not a file, so mark them all .PHONY.
.PHONY: up down ps logs smoke trino reset test lint


# Start the stack in the background, then create the buckets.
up:
	@for i in $$(seq 1 60); do docker info >/dev/null 2>&1 && break; echo "waiting for docker..."; sleep 2; done
	docker compose up -d
	PYTHONPATH=src python scripts/init_buckets.py
	#python scripts/init_buckets.py

# Stop containers. Data in ./data is kept.
down:
	docker compose down

ps:
	docker compose ps

logs:
	docker compose logs -f --tail=100

# Wait until Trino accepts queries, then run the smoke test.
smoke:
	@echo "waiting for Trino..."
	@until docker compose exec -T trino trino --execute "SELECT 1" >/dev/null 2>&1; do sleep 3; done
	docker compose exec -T trino trino --file /sql/smoke.sql

# Interactive Trino SQL shell.
trino:
	docker compose exec trino trino

# Wipe everything: containers AND all data. Rebuild with: make up, then reload.
reset:
	docker compose down
	rm -rf data

download:
	PYTHONPATH=src python -m taxi.download $(MONTH)

test:
	pytest -q

lint:
	ruff check .
load:
	PYTHONPATH=src python -m taxi.load $(MONTH)
dq:
	PYTHONPATH=src python -m taxi.quality $(MONTH)