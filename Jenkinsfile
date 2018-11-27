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

def backendImage = "tracon/tracontent:${tag}"
def staticImage = "tracon/tracontent-static:${tag}"


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
          -n tracontent-${environmentName} \
          --ignore-not-found && \
        emrichen kubernetes/jobs/setup.in.yml \
          -f kubernetes/${environmentName}.vars.yml \
          -D tracontent_tag=${tag} | \
        kubectl apply -n tracontent-${environmentName} -f -
      """
    }
  }

  stage("Deploy") {
    if (env.BRANCH_NAME == "development") {
      // Kubernetes deployment
      sh """
        emrichen kubernetes/template.in.yml \
          -f kubernetes/${environmentName}.vars.yml \
          -D tracontent_tag=${tag} | \
        kubectl apply -n tracontent-${environmentName} -f -
      """
    } else {
      // Legacy deployment
      git url: "git@github.com:tracon/ansible-tracon"
      sh """
        docker tag $backendImage tracon/tracontent:latest && \
        docker push tracon/tracontent:latest && \
        ansible-playbook \
          --vault-password-file=~/.vault_pass.txt \
          --user root \
          --limit nuoli.tracon.fi \
          --tags tracontent-deploy \
          tracon.yml
      """
    }
  }
}
