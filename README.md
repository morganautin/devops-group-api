# DevOps Group API

API REST développée avec FastAPI dans le cadre du projet de groupe DevOps.

L'objectif du projet est de mettre en place une chaîne CI/CD complète autour d'une application simple :

Code → Docker → Jenkins → SonarQube → Trivy → Registry → Terraform → Monitoring

## Fonctionnalités

L'application permet de gérer une liste simple de tâches.

Endpoints disponibles :

- `GET /` : informations générales sur l'API
- `GET /health` : vérification de l'état de l'application
- `GET /tasks` : liste des tâches
- `POST /tasks` : création d'une tâche
- `GET /metrics` : métriques Prometheus

## Technologies utilisées

- Python
- FastAPI
- Pytest
- Flake8
- Docker
- Docker Compose
- Jenkins
- SonarQube
- Trivy
- GitHub Container Registry
- Terraform
- Prometheus
- Grafana

## Lancer l'application en local

Créer un environnement virtuel :

```bash
python -m venv .venv