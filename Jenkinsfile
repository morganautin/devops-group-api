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
                    docker build -t ${IMAGE_NAME}:lint .
                    docker run --rm ${IMAGE_NAME}:lint python -m flake8 src tests
                '''
            }
        }

        stage('Build & Test') {
            steps {
                sh '''
                    docker build -t ${IMAGE_NAME}:test .

                    docker rm -f devops-group-api-test || true
                    docker create --name devops-group-api-test ${IMAGE_NAME}:test \
                        python -m pytest --cov=src --cov-report=xml

                    docker start -a devops-group-api-test
                    docker cp devops-group-api-test:/app/coverage.xml coverage.xml
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