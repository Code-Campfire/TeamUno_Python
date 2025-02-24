# Team_Uno Python Backend

## A Django REST API project for Team_Uno's project.

Setup and Installation

Create a virtual environment: `python3 -m venv venv`

Activate virtual environment: `source venv/bin/activate`

Install `pipx`
Link to pipx installation instructions: https://pipxproject.github.io/pipx/installation/

**(Outside of the project directory)**
Install Poetry (dependancy manager): `pipx install poetry`

**(Inside the project directory)**
Install dependencies:

```bash
poetry lock && poetry install
```

Running the Project

Apply database migrations: `python3 manage.py` migrate

Create a superuser (for admin access): `python3 manage.py createsuperuser`

Start the development server: `python3 manage.py runserver`

Default Endpoints

Admin interface: http://127.0.0.1:8000/admin/
API test endpoint: http://127.0.0.1:8000/api/test/
Project Structure codefire_python_backend/ ├── api/ # API application ├── codefire_python_backend/# Django project settings ├── manage.py # Django management script └── db.sqlite3 # SQLite database

### Setting up your .env files

1. Create a file named `.env.local` in the root directory of your project.
2. Add your local secret values to the `.env.local` file. For example:

**DO NOT** add secrets to the .env file in the root directory. This file is for non-sensitive values only.

### Testing the application

BEFORE TESTING:
If database changes have been made, run migrations to apply session related database changes.

Use Postman to access these endpoints:

Authorization:
Make a GET request to the base URL every time a new request is made to get a new CSRF token.

Key: X-CSRFToken
Value: **token**

Sign Up
POST
<http://127.0.0.1:8000/api/auth/signup>
this needs a body with these values to add to your database.

Body:
{
"username": "",
"email": "",
"password": ""
}

Login
POST
<http://127.0.0.1:8000/api/auth/login>

Body:
{
"username": "",
"password": ""
}

These last two endpoints use a X-CSRFToken to authorize the action.

Check Session
GET
<http://127.0.0.1:8000/api/auth/check_session>

Body:
{}

Logout
POST
<http://127.0.0.1:8000/api/auth/logout>

Body:
{}