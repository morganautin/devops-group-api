# DevOps Group API

API REST développée avec FastAPI dans le cadre du projet de groupe DevOps.

L’objectif du projet est de mettre en place une chaîne CI/CD complète autour d’une application simple, en utilisant les outils vus en cours :

```txt
Code → Docker → Jenkins → SonarQube → Trivy → Registry → Terraform → Monitoring
```

## Présentation de l’application

DevOps Group API est une API REST simple permettant de gérer une liste de tâches.

L’application a été volontairement gardée simple afin de se concentrer sur l’objectif principal du projet : construire un pipeline CI/CD complet, fonctionnel et mesurable.

## Fonctionnalités

Endpoints disponibles :

```txt
GET  /          Informations générales sur l’API
GET  /health    Vérification de l’état de l’application
GET  /tasks     Liste des tâches
POST /tasks     Création d’une tâche
GET  /metrics   Métriques Prometheus
```

L’endpoint `/health` retourne un statut `200 OK` lorsque l’application fonctionne correctement.

L’endpoint `/metrics` expose les métriques utilisées par Prometheus pour le monitoring.

## Technologies utilisées

* Python
* FastAPI
* Pytest
* Pytest-cov
* Flake8
* Docker
* Docker Compose
* Jenkins
* SonarQube
* Trivy
* GitHub Container Registry
* Terraform
* Prometheus
* Grafana

## Structure du projet

```txt
.
├── src/
│   ├── __init__.py
│   └── main.py
├── tests/
│   ├── __init__.py
│   └── test_api.py
├── infra/
│   ├── main.tf
│   ├── variables.tf
│   └── outputs.tf
├── monitoring/
│   ├── prometheus.yml
│   └── docker-compose.yml
├── Dockerfile
├── docker-compose.yml
├── Jenkinsfile
├── Makefile
├── requirements.txt
├── sonar-project.properties
└── README.md
```

## Installation locale

Créer un environnement virtuel :

```bash
python -m venv .venv
```

Activer l’environnement virtuel sous Windows PowerShell :

```bash
.\.venv\Scripts\Activate.ps1
```

Installer les dépendances :

```bash
pip install -r requirements.txt
```

Lancer l’application en local :

```bash
uvicorn src.main:app --reload
```

L’application est disponible à l’adresse :

```txt
http://localhost:8000
```

## Tester l’application

Vérifier l’endpoint de santé :

```bash
curl http://localhost:8000/health
```

Réponse attendue :

```json
{"status":"ok"}
```

## Lancer les tests unitaires

Le projet contient au moins 3 tests unitaires. Les tests sont exécutés avec Pytest et un rapport de couverture est généré au format XML.

```bash
python -m pytest --cov=src --cov-report=xml
```

Cette commande génère le fichier :

```txt
coverage.xml
```

Ce fichier est ensuite utilisé par SonarQube pour afficher la couverture de code.

## Lancer le lint

Le lint est réalisé avec Flake8 :

```bash
python -m flake8 src tests
```

Le pipeline échoue si Flake8 détecte une erreur de syntaxe ou de style bloquante.

## Commandes Makefile

Le projet contient un `Makefile` permettant de simplifier les commandes principales.

Lancer le lint :

```bash
make lint
```

Lancer les tests :

```bash
make test
```

Construire l’image Docker :

```bash
make build
```

## Lancer avec Docker

Construire l’image Docker :

```bash
docker build -t devops-group-api:latest .
```

Lancer le conteneur :

```bash
docker run -p 8000:8000 devops-group-api:latest
```

Tester l’application :

```bash
curl http://localhost:8000/health
```

## Lancer avec Docker Compose

Le fichier `docker-compose.yml` permet de lancer l’application dans un conteneur Docker avec un healthcheck et le réseau `cicd-network`.

```bash
docker compose up -d
```

Vérifier l’état du conteneur :

```bash
docker compose ps
```

Arrêter les services :

```bash
docker compose down
```

## Pipeline CI/CD Jenkins

Le fichier `Jenkinsfile` définit un pipeline CI/CD complet avec 9 stages.

Les stages du pipeline sont :

```txt
1. Checkout
2. Lint
3. Build & Test
4. SonarQube Analysis
5. Quality Gate
6. Security Scan
7. Push
8. IaC Apply
9. Smoke Test
```

### 1. Checkout

Jenkins clone le code source depuis GitHub et affiche le SHA du commit utilisé pour construire l’image.

### 2. Lint

Le code est vérifié avec Flake8 afin de détecter les erreurs de syntaxe ou de style.

### 3. Build & Test

Jenkins construit une image Docker de test, exécute les tests unitaires avec Pytest et génère un fichier `coverage.xml`.

### 4. SonarQube Analysis

Le code est analysé avec SonarQube grâce au scanner configuré dans Jenkins.

### 5. Quality Gate

Jenkins attend le résultat du Quality Gate SonarQube. Le pipeline continue uniquement si le Quality Gate est validé.

### 6. Security Scan

L’image Docker est scannée avec Trivy afin d’identifier les vulnérabilités HIGH et CRITICAL.

### 7. Push

L’image Docker est publiée sur GitHub Container Registry :

```txt
ghcr.io/morganautin/devops-group-api
```

Deux tags sont publiés :

```txt
latest
<sha-du-commit>
```

### 8. IaC Apply

Terraform est utilisé pour provisionner l’environnement de staging.

Le conteneur staging est déployé avec le nom :

```txt
devops-group-api-staging
```

Il est exposé sur le port :

```txt
8002
```

### 9. Smoke Test

Une vérification finale est réalisée sur l’endpoint `/health` après le déploiement staging.

```bash
curl -f http://devops-group-api-staging:8000/health
```

Si l’endpoint répond correctement, le pipeline est considéré comme réussi.

## SonarQube

SonarQube est utilisé pour analyser la qualité du code.

Le projet SonarQube est :

```txt
DevOps Group API
```

L’analyse permet de suivre :

```txt
Bugs
Vulnerabilities
Code Smells
Coverage
Duplications
Quality Gate
```

Dans ce projet, le Quality Gate est validé et la couverture de code est mesurable grâce au fichier `coverage.xml`.

## Trivy

Trivy est utilisé pour scanner l’image Docker et détecter les vulnérabilités.

Le scan est lancé dans le pipeline Jenkins avec la commande :

```bash
docker run --rm \
  -v /var/run/docker.sock:/var/run/docker.sock \
  aquasec/trivy:latest image \
  --severity HIGH,CRITICAL \
  --no-progress \
  --exit-code 0 \
  devops-group-api:test
```

Le rapport Trivy est visible directement dans les logs Jenkins.

## GitHub Container Registry

L’image Docker est publiée dans GitHub Container Registry.

Registry utilisé :

```txt
ghcr.io
```

Image publiée :

```txt
ghcr.io/morganautin/devops-group-api
```

## Infrastructure Terraform

Le dossier `infra/` contient la configuration Terraform permettant de déployer l’application en staging.

Fichiers Terraform :

```txt
infra/main.tf
infra/variables.tf
infra/outputs.tf
```

Terraform utilise le provider Docker pour créer :

```txt
Une image Docker
Un conteneur de staging
Une exposition du port 8002 vers le port interne 8000
Une connexion au réseau cicd-network
Un healthcheck Docker
```

Lancer Terraform manuellement :

```bash
cd infra
terraform init
terraform fmt
terraform validate
terraform apply -auto-approve -var="image_name=ghcr.io/morganautin/devops-group-api:latest"
```

Afficher les sorties Terraform :

```bash
terraform output
```

Outputs attendus :

```txt
app_url = "http://localhost:8002"
container_name = "devops-group-api-staging"
health_url = "http://localhost:8002/health"
network_name = "cicd-network"
```

## Monitoring avec Prometheus

Le dossier `monitoring/` contient la configuration Prometheus.

Fichier principal :

```txt
monitoring/prometheus.yml
```

Prometheus scrape l’endpoint suivant :

```txt
http://devops-group-api-staging:8000/metrics
```

Lancer Prometheus avec Docker :

```bash
docker run -d --name prometheus \
  --network cicd-network \
  -p 9090:9090 \
  -v ./monitoring/prometheus.yml:/etc/prometheus/prometheus.yml \
  prom/prometheus
```

Interface Prometheus :

```txt
http://localhost:9090
```

La page des targets permet de vérifier que l’application est bien scrappée :

```txt
http://localhost:9090/targets
```

Le target `devops-group-api` doit être en état `UP`.

## Monitoring avec Grafana

Grafana est utilisé pour visualiser les métriques collectées par Prometheus.

Lancer Grafana :

```bash
docker run -d --name grafana \
  --network cicd-network \
  -p 3000:3000 \
  grafana/grafana
```

Interface Grafana :

```txt
http://localhost:3000
```

Identifiants par défaut :

```txt
admin / admin
```

Source de données Prometheus à configurer dans Grafana :

```txt
http://prometheus:9090
```

Dashboard créé :

```txt
Monitoring API DevOps Group
```

Panels créés :

```txt
Total des requêtes API
Mémoire utilisée par l’API
```

Exemples de requêtes PromQL utilisées :

```promql
app_requests_total
```

```promql
process_resident_memory_bytes
```

## Lancer Prometheus et Grafana avec Docker Compose

Le dossier `monitoring/` contient aussi un fichier `docker-compose.yml` pour lancer Prometheus et Grafana.

```bash
cd monitoring
docker compose up -d
```

Arrêter les services :

```bash
docker compose down
```

## Commandes utiles

Afficher l’historique Git :

```bash
git log --oneline
```

Voir les conteneurs actifs :

```bash
docker ps
```

Tester l’application locale :

```bash
curl http://localhost:8000/health
```

Tester le staging :

```bash
curl http://localhost:8002/health
```

Tester les métriques :

```bash
curl http://localhost:8002/metrics
```

Afficher les outputs Terraform :

```bash
cd infra
terraform output
```

## Rendu du projet

Le rendu final contient :

```txt
Le lien du repository GitHub public
Un PDF avec les captures demandées
```

Captures prévues dans le PDF :

```txt
git log --oneline
Pipeline Jenkins avec les 9 stages verts
Dashboard SonarQube avec Quality Gate vert
Rapport Trivy dans les logs Jenkins
terraform output avec l’URL du staging
Prometheus targets avec l’application en statut UP
Dashboard Grafana avec au moins 2 panels
```
