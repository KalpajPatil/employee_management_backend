# 🚀 FastAPI Project Setup Guide

Welcome to your FastAPI project! Follow these steps to get up and running.

## 📋 Prerequisites

- Python 3.12 or higher installed on your system
- Git (for cloning the repository)

## 🎯 Getting Started

### Step 1: Clone the Repository

```bash
git clone https://github.com/KalpajPatil/employee_management_backend.git
cd project_root
```

### Step 2: Create a Virtual Environment

Create a virtual environment inside the root folder to isolate your project dependencies:

```bash
python -m venv .venv
```

This creates a `.venv` folder containing your virtual environment.

### Step 3: Activate the Virtual Environment

Activate your virtual environment using the appropriate command for your operating system:

**Windows (CMD):**
```cmd
.venv\Scripts\activate
```

**Windows (PowerShell):**
```powershell
.venv\Scripts\Activate.ps1
```

**macOS/Linux:**
```bash
source .venv/bin/activate
```

You should see `(.venv)` appear at the beginning of your command prompt, indicating the virtual environment is active.

### Step 4: Install Dependencies

Install all required dependencies from the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

**Current dependencies include:**
- `fastapi[standard]` - The FastAPI framework with standard extras
- `uvicorn[standard]` - ASGI server for running the application
- `SQLAlchemy` - SQL toolkit and ORM
- `pydantic` - Data validation using Python type hints
- `python-dotenv` - Environment variable management

### Step 5: Start the Application

Run the FastAPI application using Uvicorn:

```bash
uvicorn main:app --reload
```

**Command breakdown:**
- `main` refers to your `main.py` file
- `app` is the FastAPI application instance
- `--reload` enables auto-reload on code changes (development only)

### Step 6: Access Your API

Once the server starts, you can access:

- **API**: http://localhost:8000
- **Interactive API docs (Swagger UI)**: http://localhost:8000/docs
- **Alternative API docs (ReDoc)**: http://localhost:8000/redoc

## 🎨 What's Next?

- Start building your API endpoints in `main.py`
- Create models with SQLAlchemy
- Define request/response schemas with Pydantic
- Use `.env` files for configuration (loaded via python-dotenv)

## 🛑 Stopping the Server

Press `Ctrl + C` in the terminal to stop the Uvicorn server.

## 📦 Deactivating the Virtual Environment

When you're done working, deactivate the virtual environment:

```bash
deactivate
```

---

**Happy coding! 🎉**
