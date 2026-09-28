pipeline {

    agent any

    environment {
        IMAGE_NAME = 'ecommerce-api'
        IMAGE_TAG = "${BUILD_NUMBER}"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Test') {
            steps {
                sh '''
                    python3 -m venv .jenkins-venv
                    . .jenkins-venv/bin/activate
                    pip install --upgrade pip
                    pip install -r app/requirements.txt
                    pytest -v
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                    docker build \
                        --pull \
                        -t ${IMAGE_NAME}:${IMAGE_TAG} \
                        -f docker/Dockerfile .
                '''
            }
        }

        stage('Trivy Security Scan') {
            steps {
                sh '''
                    trivy image \
                        --severity HIGH,CRITICAL \
                        --format json \
                        --output trivy-report.json \
                        --exit-code 0 \
                        ${IMAGE_NAME}:${IMAGE_TAG}
                '''

                archiveArtifacts artifacts: 'trivy-report.json',
                                 fingerprint: true

                sh '''
                    trivy image \
                        --severity HIGH,CRITICAL \
                        --exit-code 1 \
                        ${IMAGE_NAME}:${IMAGE_TAG}
                '''
            }
        }
    }

    post {
        always {
            echo 'Pipeline completed.'
        }

        success {
            echo 'E-Commerce API CI pipeline succeeded.'
        }

        failure {
            echo 'E-Commerce API CI pipeline failed.'
        }
    }
}
