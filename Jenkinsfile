pipeline {
    agent any

    stages {
        stage('BuildVm') {
            steps {
		sh 'python3 -m venv venv'
                sh '. venv/bin/activate'
		sh './setup.sh'
            }
        }
	stage('Database') {
            steps {
                sh 'export USING_CONTAINER=True'
		sh 'export FLASK_ENV=Testing'
		sh './database/reset_database.sh test'
		echo 'databse setup and rest'
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
