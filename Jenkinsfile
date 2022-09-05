pipeline {
    agent any
    stages {
        stage('Env initialization') {
            steps {
                // sh 'pip3 install pytest psycopg2-binary'
                echo ('1')
            }
        }
        stage('Tests run') {
            steps {
                // sh 'pytest -v -s tests'
                echo ('2')
            }
        }
    }
    post('Allure reports') {
        always {
            script {
              /*
              allure([
                includeProperties: true,
                jdk: '',
                properties: [],
                reportBuildPolicy: 'ALWAYS',
                results: [[path: 'AllureReporting']]
              ])
              */
              echo ('3')
            }
          }
    }
}