up:
	docker compose up -d $(for) --build --force-recreate --remove-orphans

stop:
	docker compose stop $(for)

down:
	docker compose down $(for)

logs:
	docker compose logs $(for)

clear:
	docker compose down -v --rmi all --remove-orphans
