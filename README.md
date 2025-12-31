# MLOps Savings Prediction System

This project implements an end-to-end MLOps pipeline for deploying a machine learning–based savings prediction application 
in a cloud-native environment. The system uses a Streamlit web application for inference, containerized with Docker, deployed 
on Kubernetes using AWS EKS, and automated through a CI/CD pipeline built with GitHub Actions. Machine learning model artifacts 
are stored separately in Amazon S3, container images are managed in Amazon ECR, and the application is exposed via a Kubernetes
LoadBalancer. The project demonstrates real-world MLOps practices including model–code separation, automated deployments, 
Kubernetes orchestration, monitoring with Prometheus and Grafana, and cloud cost awareness.

## Tech Stack

### Cloud & Infrastructure
- Amazon Web Services (AWS)
- Amazon EKS (Elastic Kubernetes Service)
- Amazon EC2 (Worker Nodes)
- Amazon S3 (Model Artifact Storage)
- Amazon ECR (Container Registry)

### Containerization & Orchestration
- Docker
- Kubernetes

### CI/CD
- GitHub Actions

### Monitoring & Observability
- Prometheus
- Grafana

### Application & Machine Learning
- Python
- Streamlit
- scikit-learn
- joblib

## Architecture Overview

The system follows a cloud-native, microservices-oriented architecture where the machine learning application is containerized and orchestrated using Kubernetes on AWS. The application code, model artifacts, and infrastructure are decoupled to enable independent development, deployment, and scaling.

The Streamlit-based ML application is packaged as a Docker image and stored in Amazon ECR. Kubernetes, managed via Amazon EKS, pulls this image and schedules the application pod onto EC2 worker nodes. Model artifacts are stored separately in Amazon S3 and are downloaded by the application at runtime. Public access to the application is provided through a Kubernetes Service of type LoadBalancer, which provisions an AWS Elastic Load Balancer automatically.

Continuous integration and deployment are handled by GitHub Actions, which builds and pushes Docker images to ECR and updates the Kubernetes Deployment. Monitoring and observability are achieved using Prometheus for metrics collection and Grafana for visualization, both running within the same Kubernetes cluster.


