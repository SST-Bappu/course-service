pipeline {
    agent any
    environment {
        DOCKER_CREDENTIALS_ID = 'docker'
        DOCKER_IMAGE = 'sstbappu/course-service'
    }
    stages {
        stage('Checkout Code') {
            steps {
                // Pull the code from the specified branch
                git branch: 'master', url: 'https://github.com/SST-Bappu/course-service'
            }
        }
        stage('Build Docker Image') {
            steps {
                script {
                    docker.withRegistry('https://index.docker.io/v1/', "${DOCKER_CREDENTIALS_ID}") {
                        def app = docker.build("${DOCKER_IMAGE}:latest")
                        app.push()  // Pushes the Docker image to Docker Hub
                    }
                }
            }
        }
        stage('Deploy to Kubernetes') {
            steps {
                sh 'kubectl apply -f deployment.yaml'  // Deploys the Docker image to Kubernetes
            }
        }
    }
}