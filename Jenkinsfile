pipeline {
    agent any

    stages {
         stage('BuildVm') {
             steps {
	     	echo "This is Branch: ${env.BRANCH_NAME}"
		sh './setup.sh'
             }
         }
	stage('Database') {
            steps {
                sh '''. venv/bin/activate && 
			export USING_CONTAINER=True && 
			export FLASK_ENV=testing &&
			database/reset_database.sh test'''
	    }
        }
        stage('Test') {
            steps {
	    	echo 'Running tests...' 
		exprot FLASK_ENV=testing &&
		sh '''. venv/bin/activate && tests/run_tests.sh'''
            }
        }
    }
}
