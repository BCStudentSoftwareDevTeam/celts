pipeline {
    agent any

    stages {
         stage('BuildVm') {
             steps {
	     	echo "This is Pull Request: PR-${env.CHANGE_ID}"
		sh './setup.sh'
             }
         }
	stage('Database') {
            steps {
                sh '''. venv/bin/activate && 
			export USING_CONTAINER=True && 
			export FLASK_ENV=Testing &&
			database/reset_database.sh test'''
	    }
        }
        stage('Test') {
            steps {
	    	echo 'Running tests...' 
		sh '''. venv/bin/activate && tests/run_tests.sh'''
            }
        }
    }
}
