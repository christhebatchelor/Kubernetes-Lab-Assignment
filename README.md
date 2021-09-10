# Kubernetes-Lab-Assignment

## Pre-reqs
* AWS CLI (v2) is setup and configured to work with your account
* An ssh key-pair exists in ec2 (named default_key_pair unless input is modified)
* Docker desktop is installed
* Python is installed
* It's recommended to use visual studio code with YAML, Python, Docker, and CloudFormation Linter extensions installed

## Initial Build process

### Create Role
```
aws cloudformation create-stack --cli-input-yaml file://./Cloudformation/Inputs/EKS_Role_Input.yml --template-body file://./Cloudformation/Templates/EKS_Role.yml --disable-rollback --capabilities IAM_CAPABILITY
```

### Create VPC
```
aws cloudformation create-stack --cli-input-yaml file://./Cloudformation/Inputs/EKS_VPC_Input.yml --template-body file://./Cloudformation/Templates/EKS_VPC.yml --disable-rollback
```

### Create EKS Cluster
Grab the security groups, subnets, and the builder role created in the previous steps and add them to the cluster input file.
```
aws cloudformation create-stack --cli-input-yaml file://./Cloudformation/Inputs/EKS_Cluster_Input.yml --template-body file://./Cloudformation/Templates/EKS_Cluster.yml --disable-rollback
```

### Create EKS Node group
Grab the clustercontrolplane security group and the VPC and subnets from the prior steps and add them to the Node input file
```
aws cloudformation create-stack --cli-input-yaml file://./Cloudformation/Inputs/EKS_Node_Input.yml --template-body file://./Cloudformation/Templates/EKS_Node.yml --disable-rollback --capabilities IAM_CAPABILITY
```

### Update the local kubeconfig to talk to aws
```
aws eks --region us-east-2 update-kubeconfig --name helloworld-cluster
```

Grab the "NodeInstanceRole" from the Node cloudformation job and add it to the aws-auth-cm.yml file in place of the existing rolearn.

### Verify that the latest dockerub builds were successful
If the application was modified it will be necessary to ensure that the containers built successfully on dockerhub prior to proceeding with the next steps.

https://hub.docker.com/repository/docker/christsreturn/flask-test

https://hub.docker.com/repository/docker/christsreturn/nginx-test

### Use Kubectl to apply the yaml files
First aws auth
```
kubectl apply -f aws-auth-cm.yml
```
Then the services
```
kubectl apply -f flask-claim0-persistentvolumeclaim.yaml,flask-deployment.yaml,flask-service.yaml,nginx-deployment.yaml,nginx-service.yaml
```

### Use Kubectl to find the endpoint to view the "Hello World" message
Run the command below, and grab the url listed in the external-ip field for the nginx service, and paste it into your favorite web browser (or curl from the CLI).
```
kubectl get svc
```

## Technology Justification:
* Clodformation: I stuck with AWS and cloudformation because it is what I'm most familiar with. There is also plenty of documentation and support for when things go wrong. 
* EKS: Using Amazon's built in offering here seemed like the quickest way to get this up and running given I had already decided to use the aws platform and cloudformation for this project. 
* Python/flask: Python is a popular programming language with tons of support, and tutorials. The tutorial I found on creating and packaging a web application with docker used flask. 
* Kompose: I used kompose to bridge the gap between the docker-compose approach used in the python tutorial and the kubernetes platform that this assignment requested. I ran into a few roadbumps on that approach, but was ultimately able to sort them out. 
* Dockerhub: I found that even though dockercompose built my containers on the fly from the files in the repo, the yaml files created by kompose didn't do the same. I created a few repos on dockerhub, and linked them to this repo. They should auto-build assuming a recent change hasn't caused the build to break.
