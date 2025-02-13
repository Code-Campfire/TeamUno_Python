# Check if running as administrator
if (-NOT ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Write-Warning "Please run as Administrator!"
    exit
}

# Check if Chocolatey is installed
if (!(Get-Command choco -ErrorAction SilentlyContinue)) {
    Write-Host "Chocolatey is not installed. Would you like to install it? (y/n): " -NoNewline
    $install_choco = Read-Host
    if ($install_choco -match "^[Yy]$") {
        Write-Host "Installing Chocolatey..."
        Set-ExecutionPolicy Bypass -Scope Process -Force
        [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
        Invoke-Expression ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))
    } else {
        Write-Host "Chocolatey is required for this setup. Exiting..."
        exit
    }
} else {
    Write-Host "Chocolatey is already installed, skipping..."
}
# Check if PoshGit is installed
if (!(Get-Module -ListAvailable -Name posh-git)) {
    Write-Host "PoshGit is not installed. Would you like to install it? (y/n): " -NoNewline
    $install_poshgit = Read-Host
    if ($install_poshgit -match "^[Yy]$") {
        Write-Host "Installing PoshGit..."
        Install-Module posh-git -Scope CurrentUser -Force
        Import-Module posh-git
    } else {
        Write-Host "Skipping PoshGit installation..."
    }
} else {
    Write-Host "PoshGit is already installed, skipping..."
}
# PostgreSQL setup
$pgService = Get-Service postgresql* -ErrorAction SilentlyContinue
if (!$pgService) {
    Write-Host "PostgreSQL is not installed. Would you like to install it? (y/n): " -NoNewline
    $install_psql = Read-Host
    if ($install_psql -match "^[Yy]$") {
        Write-Host "Installing PostgreSQL..."
        choco install postgresql14 --params '/Password:postgres' -y
        
        # Refresh environment variables
        $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
        
        # Wait for service to be available
        Start-Sleep -Seconds 10
        
        # Create database user
        Write-Host "Enter new PostgreSQL username: " -NoNewline
        $pg_user = Read-Host
        $pg_pass = Read-Host -Prompt "Enter password for new user" -AsSecureString
        $BSTR = [System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($pg_pass)
        $plainPassword = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto($BSTR)
        
        $env:PGPASSWORD = "postgres"
        psql -U postgres -c "CREATE USER $pg_user WITH PASSWORD '$plainPassword';"
        psql -U postgres -c "CREATE DATABASE $pg_user OWNER $pg_user;"
        Remove-Item Env:\PGPASSWORD
    } else {
        Write-Host "Skipping PostgreSQL installation..."
    }
} else {
    Write-Host "PostgreSQL is already installed"
    if ($pgService.Status -ne 'Running') {
        Write-Host "PostgreSQL is not running. Starting service..."
        Start-Service postgresql*
    }
}
# Install pyenv-win
Write-Host "Installing pyenv-win..."
Invoke-WebRequest -UseBasicParsing -Uri "https://raw.githubusercontent.com/pyenv-win/pyenv-win/master/pyenv-win/install-pyenv-win.ps1" -OutFile "./install-pyenv-win.ps1"
& "./install-pyenv-win.ps1"

# Refresh environment variables
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")

# Install latest Python version using pyenv
Write-Host "Installing latest Python version..."
pyenv install -l | Select-String -Pattern '^\s*3\.\d+\.\d+$' | Select-Object -Last 1 | ForEach-Object {
    $latestVersion = $_.ToString().Trim()
    pyenv install $latestVersion
    pyenv global $latestVersion
}

# Install poetry using pip
Write-Host "Installing poetry..."
pip install poetry

# Create and activate virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1

# Install project dependencies
Write-Host "Installing project dependencies..."
poetry install

Write-Host "Setup complete! Please restart your terminal to apply all changes."