pipeline {
    agent any

    environment {
        IMAGE_NAME = 'devops-group-api'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
                sh 'git rev-parse --short HEAD'
            }
        }

        stage('Lint') {
            steps {
                sh '''
                    docker run --rm \
                        -v "$PWD":/app \
                        -w /app \
                        python:3.11-slim \
                        sh -c "pip install --no-cache-dir -r requirements.txt && python -m flake8 src tests"
                '''
            }
        }

        stage('Build & Test') {
            steps {
                sh '''
                    docker build -t ${IMAGE_NAME}:test .
                    docker run --rm ${IMAGE_NAME}:test python -m pytest --cov=src --cov-report=xml
                '''
            }
        }
    }

    post {
        always {
            sh '''
                docker rm -f devops-group-api-test || true
                docker image prune -f || true
            '''
        }

        success {
            echo 'Pipeline réussi : lint, build et tests OK.'
        }

        failure {
            echo 'Pipeline échoué : une étape doit être corrigée.'
        }
    }
}