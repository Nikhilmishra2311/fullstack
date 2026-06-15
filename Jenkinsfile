pipeline {
  agent any

  environment {
    BACKEND_IMAGE = "fullstack-backend"
    FRONTEND_IMAGE = "fullstack-frontend"
    IMAGE_TAG = "${env.GIT_COMMIT?.take(7) ?: 'latest'}"
  }

  options {
    ansiColor('xterm')
    timestamps()
    skipStagesAfterUnstable()
  }

  stages {
    stage('Checkout') {
      steps {
        checkout([
          $class: 'GitSCM',
          branches: [[name: '*/main']],
          userRemoteConfigs: [[url: 'https://github.com/Nikhilmishra2311/fullstack.git']],
        ])
      }
    }

    stage('Build Backend Image') {
      steps {
        dir('backend') {
          script {
            if (isUnix()) {
              sh "docker build -t ${BACKEND_IMAGE}:${IMAGE_TAG} ."
            } else {
              bat "docker build -t ${BACKEND_IMAGE}:${IMAGE_TAG} ."
            }
          }
        }
      }
    }

    stage('Build Frontend Image') {
      steps {
        dir('frontend') {
          script {
            if (isUnix()) {
              sh "docker build -t ${FRONTEND_IMAGE}:${IMAGE_TAG} ."
            } else {
              bat "docker build -t ${FRONTEND_IMAGE}:${IMAGE_TAG} ."
            }
          }
        }
      }
    }

    stage('Deploy') {
      steps {
        script {
          if (isUnix()) {
            sh 'docker compose down || true'
            sh 'docker compose up -d --build'
          } else {
            bat 'docker compose down || echo "Compose down failed"'
            bat 'docker compose up -d --build'
          }
        }
      }
    }
  }

  post {
    success {
      echo "Pipeline succeeded. Deployed backend:${IMAGE_TAG} and frontend:${IMAGE_TAG}."
    }
    failure {
      echo 'Pipeline failed. Check the Jenkins build log for details.'
    }
  }
}
