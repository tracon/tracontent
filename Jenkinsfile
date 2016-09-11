def image = "tracon/tracontent:build-${env.BUILD_NUMBER}"

stage("Build") {
  node {
    checkout scm
    sh "docker build --tag ${image} ."
  }
}

// stage("Test") {
//   node {
//     sh """
//       docker run \
//         --rm \
//         --link jenkins.tracon.fi-postgres:postgres \
//         --env-file ~/.tracontent.env \
//         ${image} \
//         python manage.py test --keepdb
//     """
//   }
// }

stage("Push") {
  node {
    sh "docker tag ${image} tracon/tracontent:latest && docker push tracon/tracontent:latest"
  }
}

stage("Deploy") {
  node {
    git url: "git@github.com:tracon/ansible-tracon"
    sh """
      ansible-playbook \
        --vault-password-file=~/.vault_pass.txt \
        --user root \
        --limit nuoli.tracon.fi \
        --tags tracontent-deploy \
        tracon.yml
    """
  }
}
