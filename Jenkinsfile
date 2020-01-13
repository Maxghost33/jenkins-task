def notifySlack(String buildStatus) {
    buildStatus = buildStatus ?: 'SUCCESS'
    def color
    if (buildStatus == 'SUCCESS') {
        color = '#BDFFC3'
    } else if (buildStatus == 'FAILED') {
        color = '#FF9FA1'
    }
    def msg = "${buildStatus}: `${env.JOB_NAME}` #${env.BUILD_NUMBER}:\n${env.BUILD_URL}"
    slackSend(color: color, message: msg)
}

node('docker') {
 
    stage 'Checkout'
        checkout scm
    
    stage 'Build Source Nginx (just for example - here can be (dotnet build and other))'
        sh "docker build nginx-source/ --build-arg NGINX_VERSION=1.17.7 --build-arg NJS_VERSION=0.3.6 -t ghostgoose33/nginx-source.dev"

    stage 'Docker Build Prod Image'
        imageTag = (sh (script: "git rev-parse --short HEAD", returnStdout: true))
        dockerName = "nginx-srv"
        sh "docker build . -t ghostgoose33/nginx-custom.${imageTag}"
        try{
            tagold = (sh (script: "docker ps | awk '{ print \$2 }' | grep nginx-custom", returnStdout:true))
        } catch(err){
            tagold = ""
        }
        echo "TAGOLD = ${tagold}"
        echo "IMAGETAG = ${imageTag}"
        if ("${tagold}" != ""){
            sh "docker stop ${dockerName}"
            sh "docker rm ${dockerName}"
        }
    
    stage 'Docker Run'
        sh "docker run -d -p 80:80 --network jenkins-net --name ${dockerName} ghostgoose33/nginx-custom.${imageTag}"
    
    stage 'Check NGINX'
        nginx_host = (sh (script: "docker inspect --format='{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' nginx-srv", returnStdout:true).trim())
        check_new = (sh (script: "python health-check.py ${nginx_host}", returnStdout:true).trim())
        echo "CHECK_NEW = ${check_new}"
        if ("${check_new}" != "200"){
            if ("${tagold}" == ""){
                currentBuild.result = 'FAILED'
				notifySlack(currentBuild.result)
				throw new Exception("Pipeline failed")
            }
            else{
                sh "docker push ghostgoose33/nginx-custom.${imageTag}"
				currentBuild.result = 'SUCCESS'
				notifySlack(currentBuild.result)
            }
        }
