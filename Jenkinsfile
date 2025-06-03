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

        stage('Tests') {
            parallel {
                stage('Unit') {
                    steps {
                        bat '''
                            set PYTHONPATH=%WORKSPACE%
                            coverage run --branch --source=app --omit=app\\__init__.py,app\\api.py -m pytest --junitxml=result-unit.xml test\\unit
                            coverage xml
                        '''
                        junit 'result-unit.xml'
                        stash name: 'coverage-report', includes: 'coverage.xml'
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
                        junit 'result-rest.xml'
                    }
                }

                stage('Static') {
                    steps {
                        bat '''
                            flake8 app > flake8-result.txt || exit 0
                        '''
                        recordIssues tools: [flake8()],
                            qualityGates: [
                                [threshold: 8, type: 'TOTAL', unstable: true],
                                [threshold: 10, type: 'TOTAL', failure: true]
                            ]
                    }
                }

                stage('Security Test') {
                    steps {
                        catchError(buildResult: 'UNSTABLE', stageResult: 'FAILURE') {
                            bat '''
                                bandit -r . -f custom -o bandit.out --msg-template "{abspath}:{line}: [{test_id}] {msg}" || exit 0
                            '''
                            recordIssues tools: [pyLint(name: 'Bandit', pattern: 'bandit.out')], qualityGates: [
                                [threshold: 2, type: 'TOTAL', unstable: true],
                                [threshold: 4, type: 'TOTAL', unstable: false]
                            ]
                        }
                    }
                }
            }
        }

        stage('Coverage') {
            steps {
                unstash 'coverage-report'
                recordCoverage(
                    tools: [[parser: 'COBERTURA', pattern: 'coverage.xml']],
                    sourceCodeRetention: 'EVERY_BUILD',
                    failOnError: false,
                    qualityGates: [
                        [threshold: 90.0, metric: 'LINE', baseline: 'PROJECT'],
                        [threshold: 80.0, metric: 'BRANCH', baseline: 'PROJECT']
                    ]
                )
            }
        }

        stage('Performance') {
            steps {
                catchError(buildResult: 'UNSTABLE', stageResult: 'FAILURE') {
                    bat '''
                        SET FLASK_APP=app\\api.py
                        SET FLASK_ENV=development
                        start "" /B flask run
                        ping 127.0.0.1 -n 5 >nul
                        call "C:\\apache-jmeter-5.6.3\\bin\\jmeter.bat" -n -t C:\\test-plan.jmx -l test\\results.jtl
                    '''
                    step([
                        $class: 'PerformancePublisher',
                        sourceDataFiles: 'test/results.jtl'
                    ])
                }
            }
        }
    }
}
