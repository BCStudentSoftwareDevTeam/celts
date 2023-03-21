pipeline {
    agent any

    stages {
        stage('Something 1') {
            steps {
               sh 'echo "Hello"'
               sh 'source setup.sh'
               sh 'echo "End of source setup"'
            }
        }
    }
}

