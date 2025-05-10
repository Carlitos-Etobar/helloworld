pipeline {
    agent { label 'windows' }

    stages {
        stage('Get Code') {
            steps {
                echo 'Me voy a traer el codigo'
                // Obtener código del repo
                git 'https://github.com/Carlitos-Etobar/helloworld.git'
                bat 'dir'
                echo WORKSPACE
            }
        }
        
        stage('Build') {
            steps {
                echo 'NO HAY QUE COMPILAR NADA. ESTO ES PYTHON'
            }
        }
        
        stage('Tests') {
            parallel {
                stage('Unit') {
                    steps {
                        bat '''
                            set PYTHONPATH=%WORKSPACE%
                            pytest --junitxml=result-unit.xml test\\unit
                        '''
                    }
                }
                
                stage('Rest') {
                    steps {
                        catchError(buildResult: 'UNSTABLE', stageResult: 'FAILURE') {
                            bat '''
                                SET FLASK_APP=app\\api.py
                                SET FLASK_ENV=development
                                curl -L -O https://repo1.maven.org/maven2/com/github/tomakehurst/wiremock-jre8-standalone/2.28.0/wiremock-jre8-standalone-2.28.0.jar
                                ping 127.0.0.1 -n 2 >nul
                                start "" /B flask run
                                start "" /B java -jar wiremock-jre8-standalone-2.28.0.jar --port 9090 -v --root-dir test\\wiremock
                                set PYTHONPATH=%WORKSPACE%
                                pytest --junitxml=result-rest.xml test\\rest
                            '''
                        }
                    }
                }
            }
        }
        
        stage('Results') {
            steps {
                junit 'result*.xml'
            }
        }
    }
}
