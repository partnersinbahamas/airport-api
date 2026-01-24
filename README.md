# [🛫 Airport API](https://airport-api-o8z8.onrender.com/api/v1/user/login)

REST API for managing flights, tickets, routes, airplanes, and crews.

## 🔐 Demo credentials

To log in to the site, you can use the following credentials:

- **Username:** `user`
- **Password:** `userpassword`


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

[partnersinbahamas/airport-api-app](https://hub.docker.com/repository/docker/partnersinbahamas/airport-api-app/general)

---

## 🚀 Quick Start (Docker)

### 1️⃣ Clone the repository

```bash
git clone https://github.com/your-username/airport-api.git
cd airport-api
```

---

### 2️⃣ Create `.env` and `.env.docker` file

Create a `.env` file in the project root using `.env.example`:

### .env
```env
POSTGRES_DB=your-db
POSTGRES_USER=your-user
POSTGRES_PASSWORD=your-password
POSTGRES_HOST=localhost
POSTGRES_PORT=your-port
PGDATA=your/database/url/

DJANGO_SECRET_KEY=your-secter-key
DJANGO_SETTINGS_MODULE=app.settings.dev
DJANGO_ENV=.env
```

### .env.docker
```.env.docker
POSTGRES_DB=your-db
POSTGRES_USER=your-user
POSTGRES_PASSWORD=your-password
POSTGRES_HOST=your-host
POSTGRES_PORT=your-port
PGDATA=your/database/url/

DJANGO_SECRET_KEY=your-secter-key
DJANGO_SETTINGS_MODULE=app.settings.dev
DJANGO_ENV=.env.docker

IN_DOCKER=1
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

## 🗄️ Demo database

The project includes a demo database dump.

To load demo data locally:

```bash
python manage.py loaddata db-dump.json
```

---

### 4️⃣ Open the app

API will be available at:

http://127.0.0.1:8000/
