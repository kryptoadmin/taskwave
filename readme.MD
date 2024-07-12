# Task Management Application

A task management application built using Python, Django 5, gRPC, PostgreSQL, and Docker. This application follows the Model-View-Template (MVT) architecture and includes features like task prioritization, status updates, and real-time notifications. It uses Material Design for the templates to achieve a modern look.

## Features

- Task prioritization (Low, Medium, High)
- Task status updates (Pending, In Progress, Completed)
- Real-time notifications using gRPC
- Material Design for modern UI
- Docker containerization for easy deployment

## Prerequisites

- Docker
- Docker Compose
- Python 3.10+
- PostgreSQL

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/task_management.git
cd task_management
```

### 2. Setup virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure postgresql with docker

```bash
version: '3.8'

services:
  db:
    image: postgres:13
    volumes:
      - postgres_data:/var/lib/postgresql/data/
    environment:
      POSTGRES_DB: task_management
      POSTGRES_USER: task_user
      POSTGRES_PASSWORD: password
    ports:
      - "5432:5432"

  web:
    build: .
    command: python manage.py runserver 0.0.0.0:8000
    volumes:
      - .:/code
    ports:
      - "8000:8000"
    depends_on:
      - db

volumes:
  postgres_data:
```

### 5. Configure Django to use postgresql

```bash
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'task_management',
        'USER': 'task_user',
        'PASSWORD': 'password',
        'HOST': 'db',
        'PORT': '5432',
    }
}
```

### 6. Build and Run Docker Containers

```bash
docker-compose up --build
```

### 7. Create and Apply Migrations

```bash
docker-compose exec web python manage.py makemigrations tasks
docker-compose exec web python manage.py migrate
```

### 8. Run gRPC Server

```bash
python grpc_server.py
```

### 9. Access the Application

Open your web browser and go to http://localhost:8000.
