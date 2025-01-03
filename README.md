CodeFire Python Backend
A Django REST API project for CodeFire.

Setup and Installation

Create a virtual environment: python3 -m venv venv

Activate virtual environment: source venv/bin/activate

Install dependencies: pip3 install django djangorestframework

Running the Project

Apply database migrations: python3 manage.py migrate

Create a superuser (for admin access): python3 manage.py createsuperuser

Start the development server: python3 manage.py runserver

Available Endpoints

Admin interface: http://127.0.0.1:8000/admin/
API test endpoint: http://127.0.0.1:8000/api/test/
Project Structure codefire_python_backend/ ├── api/ # API application ├── codefire_python_backend/# Django project settings ├── manage.py # Django management script └── db.sqlite3 # SQLite database