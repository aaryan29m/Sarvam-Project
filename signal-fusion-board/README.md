# 🚀 OptiToken

**Adaptive AI Cost & Token Optimization Engine featuring Dynamic Model Routing, Prompt Compression, and Semantic Caching.**

[![FastAPI](https://img.shields.io/badge/FastAPI-0.111.0-009688?style=flat&logo=fastapi)](https://fastapi.tiangolo.com)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=flat&logo=docker)](https://www.docker.com)
[![Redis](https://img.shields.io/badge/Redis-Cache-DC382D?style=flat&logo=redis)](https://redis.io)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 📌 Project Architecture
```text
optitoken/
├── frontend/
│   └── index.html        # Interactive single-file web dashboard & simulation sandbox
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI application & proxy endpoint
│   ├── config.py        # Environment settings (Pydantic v2)
│   ├── compressor.py    # Rule-based context compression
│   ├── cache.py         # Redis & memory caching engine
│   ├── router.py        # Complexity scoring & dynamic dispatcher
│   └── analytics.py     # Live savings metrics tracker
├── tests/
│   ├── test_compressor.py
│   ├── test_router.py
│   └── test_cache.py
├── .env.example
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## 🚀 Quickstart

### 1. View the Website
Simply double-click `frontend/index.html` in any web browser to open the dashboard.

### 2. Run the Backend API
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### 3. Run with Docker Compose
```bash
docker compose up --build
```
