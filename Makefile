dev:
	rm -rf ./frontend/dist && docker-compose -f ./docker/docker-compose.dev.yml up --remove-orphans
dev-new:
	rm -rf ./frontend/dist && docker-compose -f ./docker/docker-compose.dev.yml up --remove-orphans
dev-update:
	rm -rf ./frontend/dist && docker-compose -f ./docker/docker-compose.dev.yml up --build -V --remove-orphans

backend-start:
	docker build backend -t backend &&\
	docker run -it --env-file docker/.env backend
backend-test:
	docker build backend -t backend &&\
	docker run -it --env-file backend/test.env --entrypoint /code/scripts/unittest.sh backend $(file)

frontend-start:
	cd frontend && npm run dev
