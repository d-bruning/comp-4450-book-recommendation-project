# COMP 4450: Get Recc'd Book Recommendation System

## Overview

Get Recc'd is an end to end MLOps recommendation platform built with Scikit Learn, FastAPI, Streamlit, Docker, DynamoDB, AWS EC2, MLflow, Weights & Biases (W&B), GitHub Actions, and automated testing.

The system allows users to select a favorite book and receive recommendations from a KNN collaborative filtering model. The application includes:

- Recommendation engine
- FastAPI backend API
- Streamlit frontend
- Monitoring dashboard
- Docker deployment
- AWS EC2 hosting
- DynamoDB persistence
- W&B experiment tracking
- MLflow model registry
- GitHub Actions CI/CD

---

# Table of Contents

1. Overview
2. Architecture
3. Repository Structure
4. Prerequisites
5. Local Development Setup
6. Running the API
7. Running the Frontend
8. Running the Monitoring Dashboard
9. Docker Deployment
10. AWS Deployment
11. DynamoDB Setup
12. Example API Requests
13. Example User Workflow
14. Monitoring Dashboard
15. MLOps Components
16. Screenshots and Evidence
17. Troubleshooting
18. Technology Stack

---

# Architecture

## Logical Architecture

```text
User
 ↓
Streamlit Frontend
 ↓
FastAPI Backend
 ↓
KNN Recommendation Model
 ↓
DynamoDB
 ├── recommendation-cache
 └── prediction-history
```

## Cloud Deployment Architecture

```text
Application EC2 Instance
 ├── Frontend Container
 └── API Container
          ↓
      DynamoDB

Monitoring EC2 Instance
 └── Monitoring Container
          ↓
      DynamoDB
```

## Environment Configuration

Development:

```yaml
storage:
  provider: local
```

Production:

```yaml
storage:
  provider: dynamodb
```

Configuration files:

```text
src/config/
├── development.yml
├── production.yml
└── loader.py
```

---

# Repository Structure

```text
src/
├── api/
├── frontend/
├── monitoring/
├── config/
├── data/
├── models/
└── tests/

docs/
└── screenshots/
```

---

# Prerequisites

- Python 3.11+
- Docker
- Docker Compose
- Git
- AWS Account or Learner Lab

---

# Local Development Setup

Clone the repository:

```bash
git clone <repository-url>
cd comp-4450-book-recommendation-project
```

Create virtual environment:

```bash
python -m venv .venv
```

Activate:

Windows:

```powershell
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Set development environment:

```powershell
$env:ENVIRONMENT="development"
```

---

# Running the API

```bash
uvicorn src.api.main:app --reload
```

Open:

```text
http://localhost:8000/docs
```

Health check:

```text
http://localhost:8000/health
```

---

# Running the Frontend

```bash
streamlit run src/frontend/app.py
```

Open:

```text
http://localhost:8501
```

---

# Running the Monitoring Dashboard

```powershell
$env:PYTHONPATH="."
streamlit run src/monitoring/dashboard.py
```

Open:

```text
http://localhost:8502
```

---

# Docker Deployment

Build:

```bash
docker compose build
```

Start:

```bash
docker compose up -d
```

Verify:

```bash
docker ps
```

Services:

```text
API        : 8000
Frontend   : 8501
Monitoring : 8502
```

---

# AWS Deployment

## Application Instance

1. Launch EC2 instance.
2. Attach LabInstanceProfile.
3. Install Docker and Git.
4. Clone repository.
5. Provide model artifacts.
6. Set ENVIRONMENT=production.
7. Build and run Docker Compose.

Verify:

```text
http://<ec2-ip>:8000/docs
http://<ec2-ip>:8501
```

## Monitoring Instance

1. Launch second EC2 instance.
2. Attach LabInstanceProfile.
3. Clone repository.
4. Start monitoring container.

Verify:

```text
http://<monitoring-ip>:8502
```

---

# DynamoDB Setup

Create table:

```text
prediction-history
```

Partition Key:

```text
prediction_id
```

Create table:

```text
recommendation-cache
```

Partition Key:

```text
favorite_book
```

Production configuration:

```yaml
storage:
  provider: dynamodb
```

---

# Example API Requests

## Health Endpoint

Request:

```http
GET /health
```

Example:

```bash
curl http://localhost:8000/health
```

Response:

```json
{
  "status": "healthy"
}
```

## Recommendation Endpoint

Request:

```http
POST /predict
Content-Type: application/json
```

Payload:

```json
{
  "favorite_book": "The Hobbit"
}
```

cURL:

```bash
curl -X POST http://localhost:8000/predict -H "Content-Type: application/json" -d '{"favorite_book":"The Hobbit"}'
```

Example Response:

```json
{
  "favorite_book": "The Hobbit",
  "recommendations": [
    {
      "title": "Dracula",
      "author": "Bram Stoker",
      "image": "https://..."
    }
  ]
}
```

---

# Example User Workflow

1. Open Streamlit frontend.
2. Select a favorite book.
3. Click Get Recommendations.
4. View recommended books.
5. View author metadata and cover images.
6. Request is logged to DynamoDB.
7. Dashboard updates metrics.

---

# Monitoring Dashboard

Metrics:

- Total Predictions
- Unique Books
- Cache Hit Rate
- Most Requested Book
- Cached Books
- Prediction Volume
- Recent Requests

The dashboard reads local JSON files in development and DynamoDB in production.

---

# MLOps Components

## W&B

- Experiment tracking
- Hyperparameter comparison
- Model registry

## MLflow

- Experiment tracking
- Artifact management
- Model registry
- Production promotion

## GitHub Actions

- Automated test execution
- CI validation

---

# Screenshots and Evidence

This section provides visual evidence of the major components of the system, including application functionality, API validation, monitoring, cloud deployment, database integration, CI/CD automation, and MLOps tooling.

---

## Frontend

### Local Application Interface

The initial Streamlit user interface running in a local development environment.

<img src="docs/screenshots/app_1.jpg" alt="Local Streamlit application interface" width="500" />

### Recommendation Results

Example recommendation output displaying recommended books, author metadata, and cover images.

<img src="docs/screenshots/app_2.jpg" alt="Recommendation results with metadata and images" width="500" />

### AWS Frontend Deployment Verification

The Streamlit frontend successfully deployed and accessible from the AWS EC2 application instance.

<img src="docs/screenshots/aws_frontend_app_verify.jpg" alt="AWS deployed frontend application" width="500" />

---

## API

### Swagger API Documentation

Interactive FastAPI documentation generated automatically through OpenAPI.

<img src="docs/screenshots/swagger_docs.jpg" alt="FastAPI Swagger documentation" width="500" />

### Health Endpoint Verification

Verification that the FastAPI service is healthy and responding to requests.

<img src="docs/screenshots/api_health.jpg" alt="FastAPI health endpoint response" width="500" />

### Recommendation Endpoint Testing

Successful execution of the prediction endpoint.

<img src="docs/screenshots/api_predict.jpg" alt="FastAPI recommendation endpoint test" width="500" />

---

## Monitoring

### Local Monitoring Dashboard

Initial monitoring dashboard implementation using locally persisted JSON logs.

<img src="docs/screenshots/monitoring_1.jpg" alt="Local monitoring dashboard" width="500" />

### Monitoring Metrics Visualization

Operational metrics, request tracking, and cache analytics during development.

<img src="docs/screenshots/monitoring_2.jpg" alt="Monitoring metrics and analytics" width="500" />

### DynamoDB Production Monitoring

Monitoring dashboard deployed to AWS and reading production metrics directly from DynamoDB.

<img src="docs/screenshots/app_dynamo_monitoring.jpg" alt="Production monitoring dashboard using DynamoDB" width="500" />

---

## Docker

### Docker Compose Verification

Container orchestration configuration and deployment verification.

<img src="docs/screenshots/docker_compose_verify.jpg" alt="Docker Compose deployment verification" width="500" />

### Running Containers

Verification that API, Frontend, and Monitoring containers are successfully running.

<img src="docs/screenshots/docker_ps.jpg" alt="Running Docker containers" width="500" />

---

## DynamoDB

### DynamoDB Configuration

Initial DynamoDB setup and table creation.

<img src="docs/screenshots/dynamo_setup_1.jpg" alt="DynamoDB setup configuration" width="500" />

### DynamoDB Tables

Verification of the deployed DynamoDB tables.

<img src="docs/screenshots/dynamo_table_list.jpg" alt="DynamoDB table listing" width="500" />

### Recommendation Cache Evidence

Evidence of cached recommendation results being persisted to DynamoDB.

<img src="docs/screenshots/aws_cache_evidence.jpg" alt="DynamoDB recommendation cache records" width="500" />

### Prediction History Evidence

Evidence of prediction requests being logged to DynamoDB.

<img src="docs/screenshots/aws_dynamo_console.jpg" alt="DynamoDB prediction history records" width="500" />

---

## AWS Deployment

### Application EC2 Instance

Application infrastructure hosting the FastAPI API and Streamlit frontend.

<img src="docs/screenshots/aws_ec2_frontend_instance.jpg" alt="AWS EC2 application instance" width="500" />

### Monitoring EC2 Instance

Dedicated monitoring infrastructure hosting the operational dashboard.

<img src="docs/screenshots/aws_ec2_monitoring_instance.jpg" alt="AWS EC2 monitoring instance" width="500" />

---

## CI/CD

### GitHub Actions Pipeline

Successful execution of the automated CI/CD workflow including validation and testing.

<img src="docs/screenshots/cicd.jpg" alt="GitHub Actions CI/CD pipeline" width="500" />

---

## Weights & Biases (W&B)

### Experiment Tracking

Experiment comparison, evaluation metrics, and model development tracking.

<img src="docs/screenshots/wandb_experiments.jpg" alt="Weights and Biases experiment tracking" width="500" />

### Model Registry

Model registry showing tracked and versioned recommendation models.

<img src="docs/screenshots/wandb_registry.jpg" alt="Weights and Biases model registry" width="500" />

---

## MLflow

### KNN Experiment Tracking

MLflow experiment tracking for recommendation model training and evaluation.

<img src="docs/screenshots/mlflow_experiment_knn.jpg" alt="MLflow KNN experiment tracking" width="500" />

---

## DynamoDB

### DynamoDB Configuration

Initial DynamoDB setup and table creation.

<img src="docs/screenshots/dynamo_setup_1.jpg" width="500" alt="">

### DynamoDB Tables

Verification of the deployed DynamoDB tables.

<img src="docs/screenshots/dynamo_table_list.jpg" width="500" alt="">

### Recommendation Cache Evidence

Evidence of cached recommendation results being persisted to DynamoDB.

<img src="docs/screenshots/aws_cache_evidence.jpg" width="500" alt="">

### Prediction History Evidence

Evidence of prediction requests being logged to DynamoDB.

<img src="docs/screenshots/aws_dynamo_console.jpg" width="500" alt="">

---

## AWS Deployment

### Application EC2 Instance

Application infrastructure hosting the FastAPI API and Streamlit frontend.

<img src="docs/screenshots/aws_ec2_frontend_instance.jpg" width="500" alt="">

### Monitoring EC2 Instance

Dedicated monitoring infrastructure hosting the operational dashboard.

<img src="docs/screenshots/aws_ec2_monitoring_instance.jpg" width="500" alt="">

---

## CI/CD

### GitHub Actions Pipeline

Successful execution of the automated CI/CD workflow including validation and testing.

<img src="docs/screenshots/cicd.jpg" width="500" alt="">

---

## Weights & Biases (W&B)

### Experiment Tracking

Experiment comparison, evaluation metrics, and model development tracking.

<img src="docs/screenshots/wandb_experiments.jpg" width="500" alt="">

### Model Registry

Model registry showing tracked and versioned recommendation models.

<img src="docs/screenshots/wandb_registry.jpg" width="500" alt="">

---

## MLflow

### KNN Experiment Tracking

MLflow experiment tracking for recommendation model training and evaluation.

<img src="docs/screenshots/mlflow_experiment_knn.jpg" width="500" alt="">

---

# Troubleshooting

## Frontend Cannot Reach API

Verify:

```bash
uvicorn src.api.main:app --reload
```

## No DynamoDB Records

Verify:

```yaml
storage:
  provider: dynamodb
```

and confirm IAM role attachment.

## Monitoring Dashboard Failure

Verify:

```powershell
$env:PYTHONPATH="."
```

before launching Streamlit locally.

---

# Technology Stack

Machine Learning:

- Scikit Learn
- Pandas
- NumPy

Backend:

- FastAPI

Frontend:

- Streamlit

Cloud:

- AWS EC2
- DynamoDB
- IAM

MLOps:

- W&B
- MLflow
- GitHub Actions

Containers:

- Docker
- Docker Compose

Testing:

- Pytest

---

# Project Status

✅ Recommendation Engine

✅ FastAPI Backend

✅ Streamlit Frontend

✅ Monitoring Dashboard

✅ Docker Deployment

✅ AWS EC2 Deployment

✅ DynamoDB Integration

✅ W&B Tracking

✅ MLflow Registry

✅ GitHub Actions CI/CD

✅ End-to-End Production Workflow

---

# Author
Daniel Bruning

Lead Applications Developers

University of Denver Information Technology

---

# AI Transparency Note
CoPilot was used to edit and format this document.
