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
		 bat '''
		     python --version
	             python -m venv .jenkins-venv call .jenkins-venv\\Scripts\\activate.bat
		     python -m pip install --upgrade pip
		     python -m pip install -r app\\requirements.txt
		     python -m pip show fastapi
		     python -m pip show starlette
		     python -m pytest -v
	 '''
    }
}
        stage('Build Docker Image') {
            steps {
                bat '''
                    docker build ^
                        --pull ^
			--no-cache ^
                        -t %IMAGE_NAME%:%IMAGE_TAG% ^
                        -f docker\\Dockerfile .
                '''
            }
        }


	stage('Verify Docker Image') {
	   steps {
               bat '''
                    docker run --rm %IMAGE_NAME%:%IMAGE_TAG% python -c "import fastapi,starlette; print('FastAPI:', fastapi.__version__); print('Starlette:', starlette.__version__)"
        '''
    }
}

        stage('Trivy Security Scan') {
            steps {
                bat '''
                    trivy image ^
                        --severity HIGH,CRITICAL ^
                        --format json ^
                        --output trivy-report.json ^
                        --exit-code 0 ^
                        %IMAGE_NAME%:%IMAGE_TAG%
                '''

                archiveArtifacts artifacts: 'trivy-report.json',
                                 fingerprint: true

                bat '''
                    trivy image ^
                        --severity HIGH,CRITICAL ^
                        --exit-code 1 ^
                        %IMAGE_NAME%:%IMAGE_TAG%
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
