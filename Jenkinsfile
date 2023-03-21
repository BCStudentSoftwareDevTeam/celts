pipeline {
    agent {label "builtIn"}
    options {
        buildDiscarder logRotator(artifactDaysToKeepStr: '', artifactNumbToKeepStr: '5', daysToKeepStr: '', numToKeepStr: '5')
    }
    stages {
        stage('Hello') {
            steps {
                echo "Hello"
            }
        }
    }
}

