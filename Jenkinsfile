pipeline {
    agent { label 'linux' }

    stages {
        stage('Get Code') {
            steps {
                sh 'whoami && hostname && echo $WORKSPACE'
                git branch: 'develop', url: 'https://github.com/Carlitos-Etobar/helloworld.git'
            }
        }

        stage('Run REST Tests') {
            steps {
                sh '''
                    export FLASK_APP=app/api.py
                    export FLASK_ENV=development
                    nohup flask run > flask.log 2>&1 &
                    sleep 5
                    pytest --junitxml=result-rest.xml test/rest
                '''
            }
        }

        stage('Results') {
            steps {
                junit 'result-rest.xml'
            }
        }
    }
}
