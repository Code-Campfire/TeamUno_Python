# Team_Uno Python Backend

## A Django REST API project for Team_Uno's project.

Setup and Installation

pyenv and Python version instllation:

Linux/WSL:
`curl -fsSL <https://pyenv.run> | bash`

```bash
sudo apt update; sudo apt install build-essential libssl-dev zlib1g-dev \
libbz2-dev libreadline-dev libsqlite3-dev curl git \
libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev
```

MacOS:
`brew update`
`brew install pyenv`
`brew install openssl readline sqlite3 xz zlib tcl-tk@8`


Further setup:

```Bash
  echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.zshrc
  echo '[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.zshrc
  echo 'eval "$(pyenv init - zsh)"' >> ~/.zshrc
  ```
Close and reopen terminal

`pyenv install 3.13`
`pyenv global 3.13`

Create a virtual environment: `python3 -m venv python_{version number}_venv`

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

Admin interface: `http://127.0.0.1:8000/admin/`
API test endpoint: `http://127.0.0.1:8000/api/test/`
Project Structure: `codefire_python_backend/ ├── api/ # API application ├── codefire_python_backend/# Django project settings ├── manage.py # Django management script └── db.sqlite3 # SQLite database`

### Setting up your .env files

1. Create a file named `.env.local` in the root directory of your project.
2. Add your local secret values to the `.env.local` file. For example:

**DO NOT** add secrets to the `.env` file in the root directory. This file is for non-sensitive values only.

### Testing the application

BEFORE TESTING:
If database changes have been made, run migrations to apply session related database changes.

Use Postman to access application endpoints:

Authorization:
Make a GET request to the base URL every time a new request is made to get a new CSRF token.

Key: `X-CSRFToken`
Value: **token**

```JSON

Sign Up

POST
<http://127.0.0.1:8000/api/auth/signup>


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
```

These last two endpoints use a X-CSRFToken to authorize the action.

```JSON
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
```