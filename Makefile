# develop
up-db:
	docker compose -f docker-compose.yml up -d postgres --build --force-recreate --remove-orphans \
	&& docker compose up -d redis --build --force-recreate --remove-orphans

up:
	docker compose -f docker-compose.yml up -d $(for) --build --force-recreate --remove-orphans

watch:
	docker compose -f docker-compose.yml watch web

stop:
	docker compose -f docker-compose.yml stop $(for)

down:
	docker compose -f docker-compose.yml down $(for)

logs:
	docker compose -f docker-compose.yml logs $(for)

clear:
	docker compose -f docker-compose.yml down -v --rmi all --remove-orphans


# test
test-build:
	docker compose -f docker-compose.test.yml build

test-run:
	docker compose -f docker-compose.test.yml run --rm test_web

test-log:
	docker compose -f docker-compose.test.yml logs $(for)

test-clear:
	docker compose -f docker-compose.test.yml down -v --rmi all --remove-orphans
