## Setup and Deployment Instructions


This section lists all commands and configuration files used to build, deploy, and run the project from scratch.

## Prerequisites

- AWS account with required permissions
- AWS CLI installed and configured
- Docker installed
- kubectl installed
- eksctl installed
- GitHub account
- GitHub Actions enabled for the repository

---

## 1. AWS CLI Configuration

```
aws configure
```
This sets:

- AWS Access Key ID
- AWS Secret Access Key
- Default region (e.g. ap-south-1)
- Output format

## 2. Create S3 Bucket for Model Artifacts

```
aws s3 mb s3://mlops-savings-models-joblib
```
Upload model artifacts:
```
aws s3 cp random_forest_v1.joblib s3://mlops-savings-models-joblib/
aws s3 cp random_forest_features_v1.pkl s3://mlops-savings-models-joblib/
```
## 3. Build Docker Image (Local)
```
docker build -t mlops-savings-app .
```
Dockerfile location:
```
Dockerfile
```
## 4. Create Amazon ECR Repository
```
aws ecr create-repository \
  --repository-name mlops-savings-app \
  --region ap-south-1
```
Authenticate Docker with ECR:
```
aws ecr get-login-password --region ap-south-1 | \
docker login --username AWS --password-stdin \
<ACCOUNT_ID>.dkr.ecr.ap-south-1.amazonaws.com
```
## 5. Tag and Push Image to ECR
```
docker tag mlops-savings-app:latest \
<ACCOUNT_ID>.dkr.ecr.ap-south-1.amazonaws.com/mlops-savings-app:1.0
```
```
docker push <ACCOUNT_ID>.dkr.ecr.ap-south-1.amazonaws.com/mlops-savings-app:1.0
```
## 6. Create EKS Cluster
```
eksctl create cluster \
  --name mlops-cluster \
  --region ap-south-1 \
  --nodegroup-name mlops-nodes \
  --node-type t3.medium \
  --nodes 1 \
  --managed
```
Update kubeconfig:
```
aws eks update-kubeconfig \
  --name mlops-cluster \
  --region ap-south-1
```
## 7. Kubernetes Manifests

Kubernetes configuration files:
```
k8s/
├── deployment.yaml
├── service.yaml
├── configmap.yaml
├── secret.yaml.example
```
Apply ConfigMap:
```
kubectl apply -f k8s/configmap.yaml
```
Create Secret (example):
```
kubectl apply -f k8s/secret.yaml
```

Apply Deployment:
```
kubectl apply -f k8s/deployment.yaml
```

Apply Service:
```
kubectl apply -f k8s/service.yaml
```
## 8. Access the Application

Get external LoadBalancer URL:
```
kubectl get svc
```
Access the application using:
```
http://<EXTERNAL-LOADBALANCER-DNS>
```
## 9. CI/CD Pipeline (GitHub Actions)

Pipeline configuration file:
```
.github/workflows/deploy.yml
```

Pipeline steps:

- Build Docker image
- Push image to ECR
- Update Kubernetes deployment image
- Wait for rollout completion

Trigger:

- Any push to the main branch
