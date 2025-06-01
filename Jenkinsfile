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
                            pytest --junitxml=result-unit.xml test\\unit
                        '''
                        junit 'result-unit.xml'
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

                stage('Security') {
                    steps {
                        bat '''
                            bandit -r app -f xml -o bandit-result.xml || exit 0
                        '''
                        recordIssues tools: [genericParser(
                            name: 'Bandit',
                            pattern: 'bandit-result.xml',
                            script: [
                                regexp: '<issue severity="(?<severity>.*?)" confidence="(?<confidence>.*?)" text="(?<message>.*?)" test_id="(?<category>.*?)" file="(?<fileName>.*?)" line_number="(?<line>\\d+)"',
                                example: '<issue severity="LOW" confidence="HIGH" text="Use of assert detected. The enclosed code will be removed when compiling to optimised byte code." test_id="B101" file="example.py" line_number="5"'
                            ]
                        )]
                    }
                }

                stage('Coverage') {
                    steps {
                        bat '''
                            set PYTHONPATH=.
                            coverage run --branch --source=app --omit=app\\__init__.py,app\\api.py -m pytest test\\unit
                            coverage xml
                        '''
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
    }
}
