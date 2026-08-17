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
.venv\Scriptsctivate
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

## Frontend

- docs/screenshots/app_1.jpg
- docs/screenshots/app_2.jpg
- docs/screenshots/aws_frontend_app_verify.jpg

## API

- docs/screenshots/swagger_docs.jpg
- docs/screenshots/api_health.jpg
- docs/screenshots/api_predict.jpg

## Monitoring

- docs/screenshots/monitoring_1.jpg
- docs/screenshots/monitoring_2.jpg
- docs/screenshots/app_dynamo_monitoring.jpg

## Docker

- docs/screenshots/docker_ps.jpg
- docs/screenshots/docker_compose_verify.jpg

## DynamoDB

- docs/screenshots/dynamo_setup_1.jpg
- docs/screenshots/dynamo_table_list.jpg
- docs/screenshots/aws_cache_evidence.jpg
- docs/screenshots/aws_dynamo_console.jpg

## AWS

- docs/screenshots/aws_ec2_frontend_instance.jpg
- docs/screenshots/aws_ec2_monitoring_instance.jpg

## CI/CD

- docs/screenshots/cicd.jpg

## W&B and MLflow

- docs/screenshots/wandb_experiments.jpg
- docs/screenshots/wandb_registry.jpg
- docs/screenshots/mlflow_experiment_knn.jpg

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

# Author
Daniel Bruning

Lead Applications Developers

University of Denver Information Technology

# AI Transparency Note
CoPilot was used to edit and format this document.
