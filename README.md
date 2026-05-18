# DevOps + AIOps E-Commerce Monitoring Platform

A full-stack DevOps + AIOps based E-Commerce Monitoring Platform built using React, Flask, PostgreSQL, Docker, Prometheus, Grafana, and Ollama AI.

This project demonstrates:

- Full-stack application development
- Containerized microservices architecture
- AI-powered log analysis
- Monitoring and observability
- Docker orchestration
- CI/CD automation
- Real-time metrics visualization

---

# Features

## E-Commerce Features

- Add Products
- View Products
- Delete Products
- PostgreSQL Database Integration
- REST API Architecture

---

## DevOps Features

- Dockerized Frontend
- Dockerized Backend
- Dockerized PostgreSQL
- Docker Compose Orchestration
- Multi-container Infrastructure
- CI/CD with GitHub Actions

---

## Monitoring Features

- Prometheus Metrics Collection
- Grafana Monitoring Dashboard
- API Request Monitoring
- Backend CPU Usage Monitoring
- Backend Memory Usage Monitoring
- API Response Time Monitoring

---

## AIOps Features

- AI-powered Log Analysis
- Root Cause Detection
- Incident Analysis
- Automated Operational Insights
- Intelligent Troubleshooting Suggestions

---

# Tech Stack

## Frontend
- React.js
- Axios

## Backend
- Flask
- Flask-CORS
- psycopg2

## Database
- PostgreSQL

## Monitoring
- Prometheus
- Grafana

## AI / AIOps
- Ollama
- TinyLlama / Gemma / Llama3

## DevOps
- Docker
- Docker Compose
- GitHub Actions

---


# project Screenshots

## Frontend Dashboard UI

![Frontend UI](screenshots/frontend-ui.png)

![Frontend UI 2](screenshots/frontend-ui%20(1).png)

![Frontend UI 3](screenshots/frontend-ui%20(2).png)

---

## AIOps Log Analysis

![AIOps Analysis](screenshots/aiops-analysis.png)

---

## Backend API

![Backend API](screenshots/backend-api.png)

---

## Docker Containers

![Docker Containers](screenshots/docker-containers.png)

---

## Grafana Monitoring Dashboard

![Grafana Dashboard](screenshots/grafana-dashboard.png)

![Grafana Dashboard 2](screenshots/grafana-dashboard%20(2).png)

---

## Prometheus Metrics

![Prometheus Metrics](screenshots/prometheus-metrics.png)

![Prometheus Metrics 2](screenshots/prometheus-metrics%20(2).png)

![Prometheus Metrics 3](screenshots/prometheus-metrics%20(3).png)

---

## Architecture Diagram

![Architecture](screenshots/architecture.png)

# System Architecture

```text
User
   ↓
React Frontend
   ↓
Flask Backend API
   ↓
PostgreSQL Database

Flask Backend
   ↓
Prometheus Metrics
   ↓
Grafana Dashboard

Flask Backend
   ↓
Ollama AI Engine
   ↓
AIOps Log Analysis
