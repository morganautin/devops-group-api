IMAGE_NAME=devops-group-api

install:
	pip install -r requirements.txt

lint:
	python -m flake8 src tests

test:
	python -m pytest --cov=src --cov-report=xml

build:
	docker build -t $(IMAGE_NAME):latest .

up:
	docker compose up -d

down:
	docker compose down

logs:
	docker compose logs -f

health:
	curl.exe http://localhost:8000/health

metrics:
	curl.exe http://localhost:8000/metrics