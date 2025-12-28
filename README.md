# 📝 To-Do Management Application  
**FastAPI + PostgreSQL (Neon) + JWT**

A web-based **To-Do Management Application** built using **Python & FastAPI**, featuring RESTful APIs, JWT authentication, server-rendered templates, and **PostgreSQL (Neon)** as the database.  

The project intentionally avoids ORM and generic viewsets, using **raw SQL** to demonstrate low-level database control.

---

## 🚀 Features

- JWT-based authentication  
- Full CRUD operations on tasks  
- REST-compliant API design  
- Server-rendered HTML templates using **Jinja2**  
- PostgreSQL (**Neon**) database integration  
- Raw SQL (no ORM, no generic viewsets)  
- Automated API tests with **pytest**  
- Built-in API documentation (**Swagger**)  
- Logging and structured exception handling  

---

## 🛠️ Tech Stack

| Layer        | Technology              |
|--------------|--------------------------|
| Backend      | FastAPI                  |
| Database     | PostgreSQL (Neon)        |
| Authentication | JWT                    |
| Templates    | Jinja2                   |
| Testing      | pytest + httpx           |
| DB Access    | psycopg2 (raw SQL)       |
| API Docs     | Swagger (FastAPI)        |

---

## 📁 Project Structure

```text
todo_app/
│
├── app/
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── auth.py
│   ├── schemas.py
│   ├── crud.py
│   ├── routes/
│   │   ├── auth_api.py
│   │   ├── tasks_api.py
│   │   └── tasks_ui.py
│   ├── templates/
│   └── logs/
│
├── tests/
│   ├── test_auth.py
│   └── test_tasks.py
│
├── requirements.txt
├── .env
└── README.md
```

## 🔐 Authentication (JWT)

- Users authenticate via `/api/auth/login`
- A JWT access token is returned
- Token must be passed in API requests:

```http
Authorization: Bearer <JWT_TOKEN>
```

## 🗄️ Database (PostgreSQL – Neon)

### Tables

#### **users**
- `id` (PK)
- `username`
- `password`

#### **tasks**
- `id` (PK)
- `title`
- `description`
- `due_date`
- `status`
- `user_id` (FK)

> 📌 **Note:** Raw SQL is used intentionally (no ORM) to meet assignment constraints.


## ⚙️ Environment Setup

### 1️⃣ Clone Repository
```bash
git clone <your-repo-url>
cd todo_app
```

### 2️⃣ Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 🔑 Environment Variables
```bash
DATABASE_URL=postgresql://<user>:<password>@<neon-host>/<dbname>
JWT_SECRET=your_secret_key
JWT_ALGORITHM=HS256
```

### ▶️ Running the Application
```bash
uvicorn app.main:app --reload
```

- **Web UI:** http://localhost:8000  
- **Swagger Docs:** http://localhost:8000/docs  
- **OpenAPI Spec:** http://localhost:8000/openapi.json  

## 🌐 API Endpoints

### Authentication

| Method | Endpoint           | Description              |
|--------|--------------------|--------------------------|
| POST   | `/api/auth/login`  | Login and receive JWT    |

### Tasks (JWT Required)

| Method | Endpoint               | Description     |
|--------|------------------------|-----------------|
| POST   | `/api/tasks/`          | Create task     |
| GET    | `/api/tasks/`          | List tasks      |
| PUT    | `/api/tasks/{id}`      | Update task     |
| DELETE | `/api/tasks/{id}`      | Delete task     |

## 📄 Sample API Requests

### Create Task
```http
POST /api/tasks/
Authorization: Bearer <JWT>
{
  "title": "Complete assignment",
  "description": "FastAPI To-Do App",
  "due_date": "2025-01-01"
}
```

### Update Task
```http
PUT /api/tasks/1
Authorization: Bearer <JWT>
{
  "status": "completed"
}
```

### Delete Task
```http
DELETE /api/tasks/1
Authorization: Bearer <JWT>
```