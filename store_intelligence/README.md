# Apex Omni-Store Intelligence Platform
# An end-to-end Computer Vision (CV) and retail analytics engine. This system transforms raw CCTV feeds into structured operational intelligence, enabling physical retailers to track conversion funnels, zone dwell times, and operational bottlenecks with the same precision as e-commerce platforms.

# System Overview
The architecture decouples heavy CV frame processing from the analytical serving layer:

# Pipeline (pipeline/): Processes CCTV channels, applies spatial filtering (staff/noise exclusion), and streams events.

# API (app/): A FastAPI-driven ingestion engine that persists events in a relational model and serves live business metrics based on store layout and transaction logs.

# Deployment & Execution

1. Prerequisites
Python: 3.11+

# Environment: Create a .env file in the project root:

# Code snippet
# API_URL=http://127.0.0.1:8000
# DATABASE_URL=sqlite:///./store_intelligence.db
# POS_DATA_FILE=Brigade_Bangalore_10_April_26.csv
# LAYOUT_DATA_FILE=Brigade_Road_Store_layout.csv


2. Quick Start
# Install Dependencies:

# Bash
# pip install -r requirements.txt
# Launch the Backend API:

# Bash
# python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
# Execute Integration Validation:
# Run the verification harness to trigger the CV pipeline and generate analytics for multiple stores:

# Bash
# python verify_submission.py


📊 Analytics & API Reference
# The platform exposes a RESTful API for integration with store dashboards:

# POST /events/ingest: Idempotent endpoint for streaming tracking telemetry.

# GET /stores/{id}/metrics: Core KPIs (Unique Visitors, Conversion Rate, Dwell Time).

# GET /stores/{id}/funnel: Multi-stage funnel visualization (Entry → Visit → Queue → Purchase).

# GET /stores/{id}/heatmap: Spatial density mapping based on layout configuration.

# GET /stores/{id}/anomalies: Automated bottleneck detection (e.g., checkout queues).

# Once the server is live, access:

# Swagger UI: http://127.0.0.1:8000/docs

# ReDoc: http://127.0.0.1:8000/redoc

🛠️ Infrastructure & Maintenance
# Docker Support: A Dockerfile is provided for containerized deployment. Build and run using:

# Bash
# docker build -t store-intelligence .
# docker run -p 8000:8000 store-intelligence
# Logging: All pipeline execution traces and metric computations are stored in EXECUTION_LOG.txt for auditability.


### 📊 Sample System Output
Our system successfully processes multi-channel video streams and detects operational anomalies in real-time.

| Metric | Store ID: ST1008 | Store ID: ST1042 |
| :--- | :--- | :--- |
| Unique Visitors | 1347 | 615 |
| Conversion Rate | 1.78% | 13.17% |
| Bottleneck Status | CRITICAL | CLEAR |