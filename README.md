# ML Zoomcamp 2025 Midterm Project

# Project Description

## Heart Disease Prediction

This project aims to predict the presence of heart disease in patients using a dataset from the UCI Machine Learning Repository, available on Kaggle https://www.kaggle.com/datasets/johnsmith88/heart-disease-dataset/data. The dataset combines information from four different databases and contains 14 attributes is commonly used for prediction. The primary goal is to build a classification model that can determine if a patient has heart disease based on various medical attributes. This is a binary classification problem where the target variable indicates the presence (1) or absence (0) of heart disease. The analysis and model development will be done in the `notebook.ipynb` file.

The problem of predicting heart disease is a critical task in preventive medicine. The goal is to determine whether a patient has heart disease based on a set of medical attributes like age, sex, blood pressure, cholesterol levels, and other diagnostic measurements. This is a binary classification problem, where the two outcomes are either the presence or absence of heart disease.

A machine learning model can be a powerful tool in this scenario. Here's how it could be used:

1.  **Training:** A classification model (such as Logistic Regression, a Decision Tree, or a more complex ensemble model like a Random Forest or Gradient Boosting) would be trained on the provided `heart.csv` dataset. During training, the model learns the complex relationships between the patient's attributes (the features) and the final diagnosis (the target).

2.  **Prediction:** Once trained, the model can take the medical attributes of a *new* patient as input and output a prediction. This prediction would be the probability of that patient having heart disease.

3.  **Clinical Decision Support:** This predictive model can be integrated into a clinical workflow as a decision support tool. For example, a doctor could input a patient's data and get an immediate risk assessment. This can help in:
    *   **Early Diagnosis:** Identifying high-risk patients who might need further, more invasive, testing.
    *   **Prioritization:** Helping to prioritize patients in a busy clinical setting.
    *   **Personalized Medicine:** Assisting in tailoring preventive measures or treatment plans based on an individual's risk profile.

It's important to remember that such a model is a tool to assist medical professionals, not to replace their expertise and judgment. The model's predictions should be used to augment the diagnostic process.

## Setup

### Prerequisites
- Python 3.8 or higher
- uv (fast Python package installer)

### Install uv
If you don't have uv installed, install it using the official installer:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Initialize Virtual Environment
Create and activate a virtual environment using uv:

```bash
# Create a virtual environment
uv venv

# Activate the virtual environment
source .venv/bin/activate  # On macOS/Linux
# or
.venv\Scripts\activate     # On Windows
```

### Install Dependencies
Install the project dependencies:

```bash
uv pip install -r pyproject.toml
```

**Note:** This installs only the dependencies. The scripts (`train.py`, `predict.py`, `app.py`) are standalone and don't need to be installed as a package.

## Model Training

Train the model using the training script:

```bash
python train.py
```

This will generate a `model.pkl` file containing the trained model.

## Running the Application Locally

Start the Flask application:

```bash
python app.py
```

The service will be available at `http://localhost:8080`

### Test the API

```bash
curl -X POST http://localhost:8080/predict \
  -H "Content-Type: application/json" \
  -d '{
    "age": 52,
    "sex": 1,
    "cp": 2,
    "trestbps": 125,
    "chol": 212,
    "fbs": 0,
    "restecg": 1,
    "thalach": 168,
    "exang": 0,
    "oldpeak": 1.0,
    "slope": 2,
    "ca": 2,
    "thal": 3
  }'
```

## Docker Deployment

### Build the Docker Image

```bash
docker build -t heart-disease-prediction .
```

### Run the Container

```bash
docker run -p 8080:8080 heart-disease-prediction
```

## Cloud Deployment (Fly.io)

### Prerequisites
Install flyctl CLI:

```bash
# macOS/Linux
brew install flyctl

# Windows
pwsh -Command "iwr https://fly.io/install.ps1 -useb | iex"
```

### Deploy to Fly.io

1. Authenticate with Fly.io:
```bash
fly auth login
```

2. Launch the application (use once for the first lauunch):
```bash
fly launch --now
```

3. Your app will be deployed and accessible at: `https://ml-zoomcamp-2025-midterm-project.fly.dev`

### Test the Deployed Service

```bash
curl -X POST https://ml-zoomcamp-2025-midterm-project.fly.dev/predict \
  -H "Content-Type: application/json" \
  -d '{
    "age": 52,
    "sex": 1,
    "cp": 2,
    "trestbps": 125,
    "chol": 212,
    "fbs": 0,
    "restecg": 1,
    "thalach": 168,
    "exang": 0,
    "oldpeak": 1.0,
    "slope": 2,
    "ca": 2,
    "thal": 3
  }'
```

**Example Response:**
```json
{
  "heart_disease": true,
  "heart_disease_probability": 0.537055347434847
}
```

## Fly.io Service Configuration

The application is configured with cost-optimized settings suitable for development and testing. The current configuration (`fly.toml`) includes several parameters that control resource usage, scaling, and availability.

### Current Configuration Overview

**Resource Limits (Cost Control):**
- `min_machines_running = 0` - Machines automatically stop when idle to minimize costs
- `auto_stop_machines = 'stop'` - Enables automatic machine shutdown
- `auto_start_machines = true` - Automatically starts machines on incoming requests
- `memory = "1gb"` - Single GB of RAM per instance
- `size = "shared-cpu-1x"` - Single shared CPU core

**Concurrency Settings:**
- `soft_limit = 20` - Starts deprioritizing the machine after 20 concurrent requests
- `hard_limit = 25` - Stops accepting new traffic at 25 requests (returns 503)
- `type = "requests"` - Better for Flask than connection-based limiting

**Health Checks:**
- `path = "/health"` - Endpoint for health verification
- `interval = "15s"` - Health check every 15 seconds
- `grace_period = "10s"` - Allows 10 seconds for startup before checking
- `timeout = "3s"` - Health check must respond within 3 seconds

**Deployment:**
- `primary_region = "iad"` - Single region deployment (US East - Virginia)

### Performance and Resilience Improvements

For production workloads requiring better performance, higher availability, and resilience, consider the following optimizations:

#### 1. **Increase Minimum Running Instances**
```toml
min_machines_running = 2  # Always keep 2+ instances running for zero cold starts
```
**Benefits:** Eliminates cold start latency, provides immediate redundancy

#### 2. **Upgrade Machine Resources**
```toml
[[vm]]
  memory = "2gb"           # Increase for better caching and concurrent requests
  size = "shared-cpu-2x"   # More CPU for faster inference
  cpus = 2
```
**Benefits:** Handles more concurrent requests, faster model predictions

#### 3. **Adjust Concurrency Limits**
```toml
[http_service.concurrency]
  soft_limit = 50    # Handle more requests per instance
  hard_limit = 100   # Higher ceiling before rejecting traffic
```
**Benefits:** Better resource utilization, fewer 503 errors under load

#### 4. **Multi-Region Deployment**
```toml
primary_region = "iad"

[regions]
  # Add multiple regions for global redundancy
  iad = {}  # US East (Virginia)
  lhr = {}  # Europe (London)
  nrt = {}  # Asia (Tokyo)
```
**Benefits:** Lower latency for global users, automatic failover, geographic redundancy

#### 5. **Scale Count Configuration**
Add auto-scaling based on demand:
```toml
[[services.scaling]]
  min_count = 2          # Minimum instances across all regions
  max_count = 10         # Maximum instances during peak load
```
**Benefits:** Automatic scaling based on traffic patterns

#### 6. **Enhanced Health Checks**
```toml
[[http_service.checks]]
  grace_period = "30s"   # More time for model loading
  interval = "10s"       # More frequent checks
  timeout = "5s"         # Longer timeout for model inference
  path = "/health"
```
**Benefits:** More reliable health detection, fewer false positives

### Monitoring and Management Commands

Once deployed, use these commands to monitor and manage your Fly.io service:

#### **Check Application Status**
```bash
# View overall app status and running machines
fly status

# Show machine status with detailed information
fly status --all

# Check which machines are running in which regions
fly status --json | jq '.Machines[] | {id: .id, region: .region, state: .state}'
```

#### **View Application Logs**
```bash
# Stream live logs from all instances
fly logs

# Follow logs in real-time with timestamps
fly logs -f --timestamps
```

#### **Monitor Machine Health**
```bash
# Check health check status
fly checks list

# View detailed health check information
fly checks list --json
```

#### **Scale and Resource Management**
```bash
# View current scaling configuration
fly scale show

# Scale to a specific number of machines
fly scale count 3

# Scale memory for all machines
fly scale memory 2048

# Scale VMs to a different size
fly scale vm shared-cpu-2x
```

#### **View Metrics and Performance**
```bash
# Open web dashboard for detailed metrics
fly dashboard metrics

# View machine metrics (CPU, memory, network)
fly machine status <machine-id>

# List all machines with resource usage
fly machine list
```

#### **Deployment and Release Management**
```bash
# Deploy latest changes
fly deploy

# Deploy and watch logs
fly deploy --now

# Rollback to previous release
fly releases
fly rollback <version>
```

#### **SSH and Debugging**
```bash
# SSH into a running machine
fly ssh console

# SSH into specific machine
fly ssh console --select

# Run a command on a machine
fly ssh console -C "df -h"
```

#### **Resource Monitoring**
```bash
# View VM configuration
fly machines status
```

#### **Cost Monitoring**
```bash
# View current usage and estimated costs
fly dashboard

# Check machine billing status
fly machines list --json | jq '.[] | {id: .id, state: .state, region: .region}'
```

### Useful Monitoring Workflows

**Quick Health Check:**
```bash
fly status && fly checks list
```

**Monitor During Deployment:**
```bash
fly deploy && fly logs -f
```

**Check Regional Distribution:**
```bash
fly status && fly machines list
```

