pipeline {
    agent any

    environment {
        COMPOSE_PROJECT_NAME = 'smart-farming'
        REGISTRY = "${env.DOCKER_REGISTRY ?: 'docker.io'}"
        IMAGE_PREFIX = "${env.IMAGE_PREFIX ?: 'your-dockerhub-user/smart-farming'}"
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
                    sh '''
                        python3 -m venv .venv
                        . .venv/bin/activate
                        pip install -r requirements.txt
                        pytest -q
                    '''
                }
            }
        }

        stage('Frontend Build') {
            steps {
                dir('frontend') {
                    sh '''
                        npm ci || npm install
                        npm run build
                    '''
                }
            }
        }

        stage('Docker Build') {
            when {
                branch 'main'
            }
            steps {
                sh '''
                    docker compose build
                    docker tag smart-farming-backend ${IMAGE_PREFIX}-api:latest
                    docker tag smart-farming-frontend ${IMAGE_PREFIX}-web:latest
                '''
            }
        }

        stage('Push Images') {
            when {
                branch 'main'
            }
            steps {
                withCredentials([usernamePassword(credentialsId: 'docker-hub-credentials', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    sh '''
                        echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
                        docker push ${IMAGE_PREFIX}-api:latest
                        docker push ${IMAGE_PREFIX}-web:latest
                    '''
                }
            }
        }

        stage('Deploy to EC2') {
            when {
                branch 'main'
            }
            steps {
                sh '''
                    ansible-playbook -i ansible/inventory/production ansible/playbook.yml
                '''
            }
        }
    }

    post {
        always {
            cleanWs()
        }
        failure {
            echo 'Pipeline failed — check test logs and Ansible output.'
        }
    }
}
