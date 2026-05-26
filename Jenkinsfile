pipeline {
    agent any

    environment {
        COMPOSE_PROJECT_NAME = 'smart-farming'

        IMAGE_API = 'keertiibb123/smart-farming-api'
        IMAGE_WEB = 'keertiibb123/smart-farming-web'
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Backend Tests') {
            steps {
                dir('backend') {
                    bat '''
                        py -3.13 -m venv .venv

                        call .venv\\Scripts\\activate

                        python -m pip install --upgrade pip

                        pip install -r requirements.txt

                        set PYTHONPATH=.

                        python -m pytest -q
                    '''
                }
            }
        }

        stage('Frontend Build') {
            steps {
                dir('frontend') {
                    bat '''
                        npm install
                        npm run build
                    '''
                }
            }
        }

        stage('Docker Login') {
            when {
                branch 'main'
            }

            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'docker-hub-credentials',
                        usernameVariable: 'DOCKER_USER',
                        passwordVariable: 'DOCKER_PASS'
                    )
                ]) {

                    bat '''
                        echo %DOCKER_PASS% | docker login -u %DOCKER_USER% --password-stdin
                    '''
                }
            }
        }

        stage('Build Docker Images') {
            when {
                branch 'main'
            }

            steps {
                bat '''
                    docker build -t %IMAGE_API%:latest ./backend
                    docker build -t %IMAGE_WEB%:latest ./frontend
                '''
            }
        }

        stage('Push Docker Images') {
            when {
                branch 'main'
            }

            steps {
                bat '''
                    docker push %IMAGE_API%:latest
                    docker push %IMAGE_WEB%:latest
                '''
            }
        }

        stage('Deploy to EC2') {
            when {
                branch 'main'
            }

            steps {
                bat '''
                    ansible-playbook -i ansible\\inventory\\production ansible\\playbook.yml
                '''
            }
        }
    }

    post {

        always {
            cleanWs()
        }

        success {
            echo 'CI/CD Pipeline completed successfully.'
        }

        failure {
            echo 'Pipeline failed. Check Jenkins logs.'
        }
    }
}