# COMP 4450: Get Recc'd Book Recommendation System

## Overview

Get Recc'd is an end-to-end MLOps recommendation platform built with Scikit Learn, FastAPI, Streamlit, Docker, DynamoDB, AWS EC2, MLflow, Weights & Biases (W&B), GitHub Actions, and automated testing as a course project to COMP 4450 Machine Learning Operations.

The application allows users to select a favorite book and receive recommendations. The application includes:

- Recommendation engine using a KNN collaborative filtering model
- FastAPI backend API
- Streamlit frontend
- Monitoring dashboard
- Docker deployment
- AWS EC2 hosting
- DynamoDB persistence
- W&B experiment tracking and model registry
- MLflow testing and model registry
- GitHub Actions CI/CD

And, yes, I'm aware it's not the most compelling of front ends at this stage.

---

# Table of Contents

1. Dataset Selection
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
16. Screenshots
17. Troubleshooting
18. Technology Stack

---

## Dataset Selection

### Dataset Source

This project uses the Amazon Books Reviews dataset curated by Mohamed Bakhet and published on Kaggle:

https://www.kaggle.com/datasets/mohamedbakhet/amazon-books-reviews

### Dataset Description

The dataset contains book metadata and user review interactions collected from Amazon's Books category. It includes book titles, authors, ratings, and user review activity that can be used to construct recommendation systems based on user preferences and historical interactions.

### Why This Dataset Was Chosen

This dataset was selected for several reasons:

* It contains real-world user interaction data suitable for collaborative filtering and recommendation system development.
* User rating activity enables the construction of user-item interaction matrices required by recommendation algorithms such as K-Nearest Neighbors (KNN).
* The dataset aligned directly with the project objective of building a personalized book recommendation system.
* The size of the dataset is large enough to support meaningful experimentation, model evaluation, and production deployment while remaining manageable within the course project constraints.

### Data Preparation

Several preprocessing steps were performed before model training:

* Data cleaning and quality validation
* Removal of incomplete records
* Creation of a filtered 5-core dataset to improve interaction density
* Construction of a user-book interaction matrix
* Extraction and enrichment of book metadata including author names and cover images

These preprocessing steps improved recommendation quality and ensured the dataset was suitable for collaborative filtering techniques used by the production recommendation model.

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

Configuration files for local testing:

```text
src/config/
├── development.yml
├── production.yml
└── loader.py
```

Development.yml:

```yaml
storage:
  provider: local
```

production.yml:

```yaml
storage:
  provider: dynamodb
```

Note: 
docker-compose.yml overrides local src/config/loader.py config to assu

## Container Architecture

The application is deployed using a multi-container Docker architecture. Each major application component is isolated into its own container, allowing independent deployment, scaling, and maintenance.

### Container Overview

```text
docker-compose.yml
        │
        ├── FastAPI API Container
        ├── Streamlit Frontend Container
        └── Streamlit Monitoring Container
```

This separation follows MLOps best practices by decoupling model serving, user interaction, and monitoring workloads.

---

## Docker Compose Configuration

The `docker-compose.yml` file orchestrates the complete application stack and defines the relationships between containers.

### Responsibilities

* Builds container images
* Starts application services
* Configures environment variables
* Exposes required ports
* Manages inter-container communication
* Enables environment-specific deployment behavior

### Services

#### API Service

Provides model inference and backend business logic.

```text
Port: 8000
Technology: FastAPI
```

#### Frontend Service

Provides the user-facing recommendation interface.

```text
Port: 8501
Technology: Streamlit
```

#### Monitoring Service

Provides operational monitoring and recommendation quality analytics.

```text
Port: 8502
Technology: Streamlit
```

### Environment Configuration

Production deployments specify:

```yaml
environment:
  ENVIRONMENT: production
```

This automatically enables:

```text
DynamoDB storage
Production model configuration
AWS monitoring integration
```

while development deployments use:

```yaml
environment:
  ENVIRONMENT: development
```

which enables local JSON persistence.

### Verification

Successful deployment can be verified using:

```bash
docker compose up -d

docker ps
```

Reference:

<img src="docs/screenshots/docker_compose_verify.jpg" alt="Docker Compose ker_ps.jpg" alt="Runninginer

### Dockerfile.frontend

The frontend container packages the Streamlit user interface and all dependencies required to interact with the recommendation API.

### Responsibilities

* Display recommendation interface
* Send requests to FastAPI
* Collect user feedback
* Display recommendation metadata
* Display cover images

### Build Process

The container:

1. Uses a Python base image.
2. Installs required dependencies.
3. Copies application source code.
4. Exposes Streamlit port 8501.
5. Launches the Streamlit frontend application.

### Startup Command

```text
streamlit run src/frontend/app.py
```

### Exposed Port

```text
8501
```

Users access the recommendation application through this container.

Reference:

<img src="docs/screenshots/aws_frontend_app_verify.jpg" alt="AWS deployed frontend applicationitoring

The monitoring container packages the Streamlit operational dashboard used for production monitoring and recommendation quality analysis.

### Responsibilities

* Visualize prediction activity
* Monitor cache effectiveness
* Display recommendation request trends
* Display user feedback metrics
* Calculate Positive Feedback Rate

### Build Process

The container:

1. Uses a Python base image.
2. Installs monitoring dependencies.
3. Copies application source code.
4. Exposes Streamlit port 8502.
5. Launches the monitoring dashboard.

### Startup Command

```text
streamlit run src/monitoring/dashboard.py
```

### Exposed Port

```text
8502
```

The dashboard operates independently from the recommendation application and retrieves monitoring data from the configured storage provider.

The chosen deployment architecture provides several MLOps advantages:

* Separation of concerns between inference, user interaction, and monitoring.
* Independent deployment and troubleshooting of services.
* Consistent execution environments across development and production.
* Simplified cloud deployment using Docker Compose.
* Reduced configuration drift between local and AWS environments.
* Improved maintainability and scalability.

This architecture enables the complete recommendation platform to be deployed on AWS EC2 while maintaining parity between development and production environments.


---

# Repository Structure

## Repository Structure

```text
.
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── data/
│   ├── raw/
│   │   └── Source Goodreads datasets
│   │
│   └── processed/
│       └── Cleaned and transformed datasets
│
├── docs/
│   └── screenshots/
│       └── Project evidence and deployment screenshots
│
├── logs/
│   ├── prediction_logs.jsonl
│   ├── recommendation_cache.json
│   └── feedback_logs.jsonl
│
├── models/
│   ├── item_knn_model.joblib
│   └── book_index.joblib
│
├── src/
│   ├── api/
│   │   ├── main.py
│   │   ├── recommender.py
│   │   ├── schemas.py
│   │   ├── cache_service.py
│   │   ├── logging_service.py
│   │   ├── feedback_service.py
│   │   └── storage/
│   │       ├── local_storage.py
│   │       └── dynamodb_storage.py
│   │
│   ├── config/
│   │   ├── development.yml
│   │   ├── production.yml
│   │   └── loader.py
│   │
│   ├── frontend/
│   │   ├── app.py
│   │   └── assets/
│   │       └── default-book.svg
│   │
│   ├── monitoring/
│   │   ├── dashboard.py
│   │   ├── monitoring_service.py
│   │   └── storage/
│   │       ├── local_monitoring_storage.py
│   │       └── dynamodb_monitoring_storage.py
│   │
│   ├── preprocessing/
│       ├── breakdowns.py
│       ├── data_5core_filter.py
│       ├── data_5core_report.py
│       ├── dataset_profile.py
│       ├── metadata.py
│       └── trimmer.py
│   │
│   └── training/
│       ├── mlflow_utils.py
│       ├── train_item_knn.py
│       ├── train_item_knn_mlflow.py
│       ├── train_popularity_baseline.py
│       ├── train_popularity_baseline_mlflow.py
│       ├── train_popularity_top100.py
│       ├── validate_item_knn.py
│       └── wandb_test.py
│
├── tests/
│   ├── test_health.py
│   ├── test_predict.py
│   └── manual_test_recommender.py
│
├── Dockerfile.frontend
├── Dockerfile.monitoring
├── docker-compose.yml
├── requirements.txt
├── mlflow.db
├── ruff.toml
├── test_mlflow.py
├── wandb_test.py
└── README.md
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

The monitoring dashboard provides operational visibility into the recommendation system and serves as the primary observability interface for production deployments.

The dashboard reads from the configured storage provider:

* Development: local JSON log files
* Production: Amazon DynamoDB

Monitored metrics include:

* Total Predictions
* Unique Books Requested
* Cache Hit Rate
* Cached Books
* Most Requested Book
* Prediction Volume Over Time
* Top Requested Books
* Recent Prediction Requests
* Total Feedback
* Positive Feedback Rate
* User Feedback Distribution

In addition to operational metrics, the dashboard supports recommendation quality monitoring through a user feedback pipeline. Users can submit positive or negative feedback on recommendation usefulness directly from the frontend application. Feedback is persisted through the application's storage layer and surfaced within the monitoring dashboard.

This feedback loop enables ongoing evaluation of recommendation quality in production and provides a live measure of recommendation usefulness through the Positive Feedback Rate metric.

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

# Screenshots

This section provides visual evidence of the major components of the system, including application functionality, API validation, monitoring, cloud deployment, database integration, CI/CD automation, and MLOps tooling per project requirements.

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

### User Feedback

Example user feedback submission through the recommendation interface. Users can provide positive or negative feedback on recommendation quality, allowing the system to collect live production feedback for monitoring and evaluation purposes.

<img src="docs/screenshots/user_feedback.jpg" alt="User feedback on recommendation results." />

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

### User Feedback Monitoring

Monitoring dashboard displaying collected user feedback and recommendation quality metrics.

<img src="docs/screenshots/user_feedback_monitoring.jpg" alt="Feedback monitoring metrics and analytics" width="500" />

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

### Recommendation Cache

Evidence of cached recommendation results being persisted to DynamoDB.

<img src="docs/screenshots/aws_cache_evidence.jpg" alt="DynamoDB recommendation cache records" width="500" />

### Prediction History

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

### Recommendation Cache

Evidence of cached recommendation results being persisted to DynamoDB.

<img src="docs/screenshots/aws_cache_evidence.jpg" width="500" alt="">

### Prediction History

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
