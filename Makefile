.PHONY: build up down migrations migrate superuser
build:
	docker-compose build
up:
	docker-compose up && docker-compose rm -fsv
down:
	docker-compose down --volumes
migrations:
	python manage.py makemigrations
migrate:
	docker-compose run web python3 manage.py migrate
superuser:
	docker-compose run web python3 manage.py createsuperuser
test:
	docker-compose run web pytest --ds=core.settings --reuse-db -s
