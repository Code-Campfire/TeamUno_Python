#!/bin/bash

# Check if Homebrew is installed
if ! command -v brew &> /dev/null; then
    read -p "Homebrew is not installed. Would you like to install it? (y/n): " install_brew
    if [[ $install_brew =~ ^[Yy]$ ]]; then
        echo "Installing Homebrew..."
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    else
        echo "Homebrew is required for this script. Exiting..."
        exit 1
    fi
fi

# Check if zsh is already installed
if ! command -v zsh &> /dev/null; then
    read -p "zsh is not installed. Would you like to install it? (y/n): " install_zsh
    if [[ $install_zsh =~ ^[Yy]$ ]]; then
        echo "Installing zsh..."
        brew install zsh
        chsh -s $(which zsh)
    else
        echo "Skipping zsh installation..."
    fi
else
    echo "zsh is already installed, skipping..."
fi

# Check if Oh My Zsh is installed
if [ ! -d "$HOME/.oh-my-zsh" ]; then
    read -p "Oh My Zsh is not installed. Would you like to install it? (y/n): " install_omz
    if [[ $install_omz =~ ^[Yy]$ ]]; then
        echo "Installing Oh My Zsh..."
        sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
    else
        echo "Skipping Oh My Zsh installation..."
    fi
else
    echo "Oh My Zsh is already installed, skipping..."
fi
# PostgreSQL setup
if ! command -v psql &> /dev/null; then
    read -p "PostgreSQL is not installed. Would you like to install it? (y/n): " install_psql
    if [[ $install_psql =~ ^[Yy]$ ]]; then
        echo "Installing PostgreSQL..."
        sudo apt install postgresql postgresql-contrib -y
        sudo systemctl enable postgresql
        sudo systemctl start postgresql
        
        # Create database user
        read -p "Enter new PostgreSQL username: " pg_user
        sudo -u postgres createuser --interactive --pwprompt $pg_user
        sudo -u postgres createdb $pg_user
    else
        echo "Skipping PostgreSQL installation..."
    fi
else
    echo "PostgreSQL is already installed"
    if ! systemctl is-active --quiet postgresql; then
        echo "PostgreSQL is not running. Starting service..."
        sudo systemctl start postgresql
    fi
fi
# pyenv setup
if ! command -v pyenv &> /dev/null; then
    echo "Installing pyenv..."
    brew install pyenv
fi

echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.zshrc
echo '[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.zshrc
echo 'eval "$(pyenv init - zsh)"' >> ~/.zshrc
exec "$SHELL"

# Latest Python version setup
pyenv install
PYTHON_VERSION=$(pyenv version-name)
pyenv global $PYTHON_VERSION
python3 -m venv venv

# pipx setup and poetry setup
brew install pipx
pipx ensurepath
pipx install poetry
exec "$SHELL"

poetry lock && poetry install