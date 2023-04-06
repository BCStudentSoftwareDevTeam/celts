pipeline {
    agent any

    stages {
         stage('BuildVm') {
             steps {
		sh './setup.sh'
             }
         }
	stage('Database') {
            steps {
                sh '''venv/bin/activate && 
			export USING_CONTAINER=True && 
			export FLASK_ENV=Testing &&
			database/reset_database.sh test'''
	    }
        }
        stage('Test') {
            steps {
	    	 bash '''venv/bin/activate && tests/run_test.sh'''
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
