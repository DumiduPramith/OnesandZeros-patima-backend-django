.PHONY: docker-build
docker-build:
	docker compose -f docker-compose.prod.yml build

.PHONY: docker-up
docker-up:
	docker compose -f docker-compose.prod.yml up


.PHONY: docker-up-d
docker-up-d:
	docker compose -f docker-compose.prod.yml up -d

.PHONY: docker-down
docker-down:
	docker compose -f docker-compose.prod.yml down

.PHONY: docker-initial
docker-initial:
	docker exec patima-backend sh -c "make create-tables && make initial-data && make collect-static"