up-db:
	docker compose up -d postgres --build --force-recreate --remove-orphans \
	&& docker compose up -d redis --build --force-recreate --remove-orphans

up:
	docker compose up -d $(for) --build --force-recreate --remove-orphans

watch:
	docker compose watch web

stop:
	docker compose stop $(for)

down:
	docker compose down $(for)

logs:
	docker compose logs $(for)

clear:
	docker compose down -v --rmi all --remove-orphans
