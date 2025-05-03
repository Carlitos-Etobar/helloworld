pipeline {
    agent any

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
                                start "" /B flask run
                                start "" /B java -jar F:\\Agentes\\wiremock-jre8-standalone-2.28.0.jar --port 9090 -v --root-dir F:\\Repositorios\\helloworld\\test\\wiremock
                                
                                REM Check del puerto 5000 para flask
                                :wait_for_flask
                                for /f "tokens=5" %%a in ('netstat -ano ^| find ":5000" ^| find "LISTENING"') do (
                                    goto flask_ready
                                )
                                ping 127.0.0.1 -n 2 >nul
                                goto wait_for_flask
                                :flask_ready
                                
                                REM Check del puerto 9090 para wiremock
                                :wait_for_wiremock
                                for /f "tokens=5" %%a in ('netstat -ano ^| find ":9090" ^| find "LISTENING"') do (
                                    goto wiremock_ready
                                )
                                ping 127.0.0.1 -n 2 >nul
                                goto wait_for_wiremock
                                :wiremock_ready
                                
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
