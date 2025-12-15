# FastAPI Application

This repository contains a **FastAPI** application that can be run **locally** or using **Docker**.

---

## Requirements

### For Local Development

* Python **3.9+**
* `pip`
* (Recommended) `virtualenv` or `venv`

### For Docker

* Docker **20+**
* Docker Compose (optional but recommended)

---

## Project Structure (Example)

```text
.
├── app/
│   ├── main.py          # FastAPI entry point
│   ├── __init__.py
│   └── routers/
├── requirements.txt
├── Dockerfile
├── docker-compose.yml   # optional
└── README.md
```

---

## Running the App Locally

### 1. Clone the Repository

```bash
git clone https://github.com/Proac-Tee/fastapi-server-template.git
cd fastapi-server-template
```

### 2. Create and Activate a Virtual Environment

```bash
python -m venv venv

# Linux / macOS
source venv/bin/activate

# Windows
venv\\Scripts\\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Application

```bash
uvicorn app.main:app --reload
```

The API will be available at:

* **API:** [http://127.0.0.1:8000](http://127.0.0.1:8000)
* **Swagger UI:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
* **ReDoc:** [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## Running the App with Docker

### 1. Build the Docker Image

```bash
docker build -t fastapi-app .
```

### 2. Run the Container

```bash
docker run -d \
  --name fastapi-container \
  -p 8000:8000 \
  fastapi-app
```

The API will be available at:

* [http://localhost:8000](http://localhost:8000)

---

## Running with Docker Compose (Optional)

If you are using `docker-compose.yml`:

```bash
docker-compose up --build
```

To stop the services:

```bash
docker-compose down
```

---

## Example Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## Environment Variables

You can use environment variables for configuration.

Example:

```bash
export ENV=development
export DATABASE_URL=postgresql://user:password@localhost/db
```

Or with Docker:

```bash
docker run
```
