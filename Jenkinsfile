pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                sh 'source setup.sh'
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
