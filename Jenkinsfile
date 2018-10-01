
// Variable ; don't seem working with docker.build
def dockerName='repo.x3rus.com/xerus/x3-sip-dir-srv'

def app

pipeline {
    agent any

        stages {

            stage('Unittest') {
                steps {
                    /* use unittest */
                    script {
                       sh 'python3 unittestSip.py'
                    }
                }
            }

            stage('Build image') {
                steps {
                    /* This builds the actual image; synonymous to
                     * docker build on the command line */
                    script {
                        app = docker.build('repo.x3rus.com/xerus/x3-sip-dir-srv')
                    }
                }
            }


        } // END stages

    post {
        success {
            script {
                docker.withRegistry('https://repo.x3rus.com', 'repo-x3rus-com_credential') {
                    app.push("${env.BUILD_ID}")
                    // Disable push latest to push it after remote validation
                    app.push("latest")
                }
            }
        }
        failure {
            echo 'Email me'
        }
    } // END POST       

} // END pipeline 
