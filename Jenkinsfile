pipeline {
    agent any

    options {
        timestamps()
        disableConcurrentBuilds()
    }

    environment {
        COMPOSE_PROJECT_NAME = 'wecareforyou'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Frontend Build') {
            steps {
                dir('frontend') {
                    sh 'npm ci'
                    sh 'npm run build'
                }
            }
        }

        stage('Backend Syntax Check') {
            steps {
                dir('backend') {
                    sh 'python3 -m compileall .'
                }
            }
        }

        stage('Docker Build') {
            steps {
                sh 'docker compose build'
            }
        }

        stage('Deploy') {
            when {
                branch 'main'
            }
            environment {
                DATABASE_URL = credentials('wecare-database-url')
                SECRET_KEY = credentials('wecare-secret-key')
                JWT_SECRET_KEY = credentials('wecare-jwt-secret-key')
            }
            steps {
                sh 'chmod +x scripts/jenkins-deploy.sh'
                sh './scripts/jenkins-deploy.sh'
            }
        }
    }

    post {
        always {
            sh 'docker compose ps || true'
        }
        failure {
            sh 'docker compose logs --tail=120 || true'
        }
    }
}
