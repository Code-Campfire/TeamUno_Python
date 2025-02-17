# Check if zsh is already installed
if ! command -v zsh &> /dev/null; then
    read -p "zsh is not installed. Would you like to install it? (y/n): " install_zsh
    if [[ $install_zsh =~ ^[Yy]$ ]]; then
        echo "Installing zsh and zplug..."
        sudo apt install zsh zplug -y
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
        sudo service postgresql enable
        sudo service postgresql start

        sleep 5  # Wait for PostgreSQL to start
        
        # Create database user
        read -p "Enter new PostgreSQL username: " pg_user
        sudo -u postgres createuser --interactive --pwprompt $pg_user
        sudo -u postgres createdb $pg_user
    else
        echo "Skipping PostgreSQL installation..."
    fi
else
    echo "PostgreSQL is already installed"
    if ! service postgresql status > /dev/null 2>&1; then
        echo "PostgreSQL is not running. Starting service..."
        sudo service postgresql start
        sleep 5  # Wait for PostgreSQL to start
    fi
fi
# pyenv setup
curl -fsSL https://pyenv.run | bash;
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
python3 -m pip install --user pipx
python3 -m pipx ensurepath
sudo pipx ensurepath --global
pipx install poetry
exec "$SHELL"
poetry lock && poetry install