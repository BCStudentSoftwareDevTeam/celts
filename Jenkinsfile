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
                sh '''. venv/bin/activate && 
			export USING_CONTAINER=True && 
			export FLASK_ENV=Testing &&
			database/reset_database.sh test'''
	    }
        }
        stage('Test') {
            steps {
	    	echo 'Running tests... 3:02' 
		sh '''. venv/bin/activate && tests/run_tests.sh'''
            }
        }
    }
}
