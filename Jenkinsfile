def appName = "tracontent"

def imageMap = [
  "development": "staging",
  "master": "latest"
]

def environmentNameMap = [
  "master": "production",
  "development": "staging"
]

def tag = "${env.BRANCH_NAME}-${env.BUILD_NUMBER}"
def environmentName = environmentNameMap[env.BRANCH_NAME]
def namespace = "${appName}-${environmentName}"

def backendImage = "tracon/${appName}:${tag}"
def staticImage = "tracon/${appName}-static:${tag}"


node {
  stage("Build") {
    checkout scm
    sh "docker build --tag $backendImage ."
    sh "docker build --file Dockerfile.static --build-arg BACKEND_IMAGE=$backendImage --tag $staticImage ."
  }

  stage("Push") {
    sh """
      docker push $backendImage && \
      docker push $staticImage
    """
  }

  stage("Setup") {
    if (env.BRANCH_NAME == "development") {
      sh """
        kubectl delete job/setup \
          -n ${namespace} \
          --ignore-not-found && \
        emrichen kubernetes/jobs/setup.in.yml \
          -f kubernetes/${environmentName}.vars.yml \
          -D ${appName}_tag=${tag} | \
        kubectl apply -n ${namespace} -f - && \
        kubectl wait --for condition=complete -n ${namespace} job/setup
      """
    }
  }

  stage("Deploy") {
    if (env.BRANCH_NAME == "development") {
      // Kubernetes deployment
      sh """
        emrichen kubernetes/template.in.yml \
          -f kubernetes/${environmentName}.vars.yml \
          -D ${appName}_tag=${tag} | \
        kubectl apply -n ${namespace} -f - && \
        kubectl wait -n ${namespace} --for condition=Ready --selector build=${tag} pod
      """
    } else {
      // Legacy deployment
      git url: "git@github.com:tracon/ansible-tracon"
      sh """
        docker tag $backendImage tracon/${appName}:latest && \
        docker push tracon/${appName}:latest && \
        ansible-playbook \
          --vault-password-file=~/.vault_pass.txt \
          --user root \
          --limit nuoli.tracon.fi \
          --tags ${appName}-deploy \
          tracon.yml
      """
    }
  }
}
