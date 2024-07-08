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


.PHONY: docker-full-clear
docker-full-clear:
	@containers=$$(docker ps -aq); \
	if [ -n "$$containers" ]; then \
		docker rm $$containers; \
	fi

	@images=$$(docker images -q); \
	if [ -n "$$images" ]; then \
		docker rmi $$images; \
	fi

	@volumes=$$(docker volume ls -q); \
	if [ -n "$$volumes" ]; then \
		docker volume rm $$volumes; \
	fi
