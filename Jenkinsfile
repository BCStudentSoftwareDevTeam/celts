pipeline {
    agent any

    stages {
        stage('BuildVm') {
            steps {
// 		sh 'python3 -m venv venv'
//                 sh '. venv/bin/activate'
            }
        }
	stage('Database') {
            steps {
                sh './setup.sh && export USING_CONTAINER=True && export FLASK_ENV=Testing && ./database/reset_database.sh test'
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
