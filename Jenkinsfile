pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
		sh 'source setup.sh'
		sh './setup.sh'
                sh 'cd database/'
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
