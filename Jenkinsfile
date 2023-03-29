pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                sh 'cd database/'
		sh 'which python'
		sh 'python --version'
            }
        }
        stage('Test') {
            steps {
                echo 'Testing..'
            }
        }
        stage('Deploy') {
            steps {
                echo 'Deploying....'
            }
        }
    }
}
