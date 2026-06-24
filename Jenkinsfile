pipeline {
    agent any

    environment {
        IMAGE_NAME = 'devops-group-api'
        REGISTRY = 'ghcr.io/morganautin'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
                script {
                    env.IMAGE_TAG = sh(
                        script: 'git rev-parse --short HEAD',
                        returnStdout: true
                    ).trim()
                }
                sh 'git rev-parse --short HEAD'
                echo "Image tag : ${env.IMAGE_TAG}"
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

        stage('Push') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'github-token',
                        usernameVariable: 'GHCR_USER',
                        passwordVariable: 'GHCR_TOKEN'
                    )
                ]) {
                    sh '''
                        echo "$GHCR_TOKEN" | docker login ghcr.io -u "$GHCR_USER" --password-stdin

                        docker tag ${IMAGE_NAME}:test ${REGISTRY}/${IMAGE_NAME}:${IMAGE_TAG}
                        docker tag ${IMAGE_NAME}:test ${REGISTRY}/${IMAGE_NAME}:latest

                        docker push ${REGISTRY}/${IMAGE_NAME}:${IMAGE_TAG}
                        docker push ${REGISTRY}/${IMAGE_NAME}:latest

                        docker logout ghcr.io
                    '''
                }
            }
        }

        stage('IaC Apply') {
            steps {
                sh '''
                    docker rm -f devops-group-api-staging || true

                    docker run --rm \
                        --volumes-from jenkins \
                        -v /var/run/docker.sock:/var/run/docker.sock \
                        -w "$PWD/infra" \
                        hashicorp/terraform:latest init

                    docker run --rm \
                        --volumes-from jenkins \
                        -v /var/run/docker.sock:/var/run/docker.sock \
                        -w "$PWD/infra" \
                        hashicorp/terraform:latest fmt -check

                    docker run --rm \
                        --volumes-from jenkins \
                        -v /var/run/docker.sock:/var/run/docker.sock \
                        -w "$PWD/infra" \
                        hashicorp/terraform:latest validate

                    docker run --rm \
                        --volumes-from jenkins \
                        -v /var/run/docker.sock:/var/run/docker.sock \
                        -w "$PWD/infra" \
                        hashicorp/terraform:latest apply -auto-approve \
                        -var="image_name=${REGISTRY}/${IMAGE_NAME}:${IMAGE_TAG}"

                    docker run --rm \
                        --volumes-from jenkins \
                        -v /var/run/docker.sock:/var/run/docker.sock \
                        -w "$PWD/infra" \
                        hashicorp/terraform:latest output
                '''
            }
        }

        stage('Smoke Test') {
            steps {
                sh '''
                    sleep 10
                    curl -f http://devops-group-api-staging:8000/health
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
            echo "Pipeline réussi ! Image publiée, staging déployé et smoke test OK : ${REGISTRY}/${IMAGE_NAME}:${IMAGE_TAG}"
        }

        failure {
            echo 'Pipeline échoué : une étape doit être corrigée.'
        }
    }
}