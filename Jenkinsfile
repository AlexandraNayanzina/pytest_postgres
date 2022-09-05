pipeline {
    agent any
    stages {
        stage('build') {
            steps {
                sh '''
                    python3 -m venv venv
                    source  venv/bin/activate
                    pip install -r requirements.txt
                    pytest -v -s --alluredir AllureReports tests
                '''
            }
        }
    }
    post('Allure reports') {
        always {
            script {
              allure([
                includeProperties: true,
                jdk: '',
                properties: [],
                reportBuildPolicy: 'ALWAYS',
                results: [[path: 'AllureReports']]
              ])
            }
          }
    }
}