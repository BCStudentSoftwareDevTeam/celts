pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
		sh 'sudo apt-get install python3-venv'
		sh 'python3 -m venv venv'
                sh '. venv/bin/activate'
		sh './setup.sh'
		sh 'export USING_CONTAINER=True'
		sh 'export FLASK_ENV=Testing'
		sh './database/reset_database.sh test'
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
