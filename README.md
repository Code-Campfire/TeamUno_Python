# Team_Uno Python Backend

## A Django REST API project for Team_Uno's project.

### SSH Key Setup

#### For Unix-based Systems (Linux/MacOS/WSL)

1. Generate SSH key: `ssh-keygen -t ed25519 -C "your_email@example.com"`
2. Start ssh-agent: `eval "$(ssh-agent -s)"`
3. Add SSH key to agent: `ssh-add ~/.ssh/id_ed25519`
4. Copy key to clipboard: `cat ~/.ssh/id_ed25519.pub | pbcopy` (Mac) or `cat ~/.ssh/id_ed25519.pub | xclip -selection clipboard` (Linux)

#### For Windows (PowerShell)

1. Open PowerShell
2. Generate SSH key: `ssh-keygen -t ed25519 -C "your_email@example.com"`
3. Start ssh-agent:

    ```powershell
    Get-Service ssh-agent | Set-Service -StartupType Manual
    Start-Service ssh-agent
    ```

4. Add SSH key to agent: `ssh-add $HOME/.ssh/id_ed25519`
5. Copy key to clipboard: `Get-Content $HOME/.ssh/id_ed25519.pub | Set-Clipboard`

Clone the repo: `git clone <git@github.com>:Code-Campfire/TeamUno_Python.git`

#### Add Key to GitHub

1. Go to GitHub Settings > SSH and GPG keys
2. Click "New SSH key"
3. Paste your key and save

Test connection: `ssh -T git@github.com`

### Setup and Installation

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

Available Endpoints

Admin interface: http://127.0.0.1:8000/admin/
API test endpoint: http://127.0.0.1:8000/api/test/
Project Structure codefire_python_backend/ ├── api/ # API application ├── codefire_python_backend/# Django project settings ├── manage.py # Django management script └── db.sqlite3 # SQLite database

### Setting up your .env files

1. Create a file named `.env.local` in the root directory of your project.
2. Add your local secret values to the `.env.local` file. For example:

**DO NOT** add secrets to the .env file in the root directory. This file is for non-sensitive values only.