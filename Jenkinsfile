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

                    sed -i 's#/app/src#src#g' coverage.xml || true
                '''
            }
        }

        stage('SonarQube Analysis') {
            steps {
                script {
                    def scannerHome = tool 'SonarScanner'
                    withSonarQubeEnv('SonarQube') {
                        sh "${scannerHome}/bin/sonar-scanner"
                    }
                }
            }
        }

        stage('Quality Gate') {
            steps {
                timeout(time: 2, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: true
                }
            }
        }

        stage('Security Scan') {
            steps {
                sh '''
                    docker run --rm \
                        -v /var/run/docker.sock:/var/run/docker.sock \
                        aquasec/trivy:latest image \
                        --severity HIGH,CRITICAL \
                        --no-progress \
                        --exit-code 0 \
                        ${IMAGE_NAME}:test
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
            echo 'Pipeline réussi : lint, build, tests, SonarQube et scan Trivy OK.'
        }

        failure {
            echo 'Pipeline échoué : une étape doit être corrigée.'
        }
    }
}