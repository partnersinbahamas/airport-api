# 🛫 Airport API

REST API for managing flights, tickets, routes, airplanes, and crews.

---
## 📦 Tech Stack

- Python 3.12
- Django + Django REST Framework
- PostgreSQL 16
- Docker & Docker Compose
- Gunicorn (production-ready)
- pytest (tests)

---

## 🗄 Database

- PostgreSQL runs inside a Docker container
- Database data is persisted in a Docker volume (app-db)
- Default port mapping: 5436 → 5432

---

## 🐳 Docker Images

The application image is published on Docker Hub: 

**partnersinbahamas/airport-api-app**

---

## 🚀 Quick Start (Docker)

### 1️⃣ Clone the repository

```bash
git clone https://github.com/your-username/airport-api.git
cd airport-api
```

---

### 2️⃣ Create `.env` file

Create a `.env` file in the project root using `.env.example`:

```env
POSTGRES_DB=
POSTGRES_USER=
POSTGRES_PASSWORD=
POSTGRES_HOST=
POSTGRES_PORT=
PGDATA=
LOCAL_POSTGRES_HOST=localhost
LOCAL_POSTGRES_PORT=
```

---

### 3️⃣ Build and run containers

```bash
docker-compose build
```

```bash
docker-compose up
```

This command will:
- build the Django image
- start PostgreSQL
- apply migrations
- collect static files
- run the development server

---

### 4️⃣ Open the app

API will be available at:

http://127.0.0.1:8000/
