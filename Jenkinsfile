pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                sh 'cd database/'
		echo 'hello...'
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
