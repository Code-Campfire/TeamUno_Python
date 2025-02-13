import os
import subprocess
import sys
from pathlib import Path

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def run_setup_script(script_name: str) -> None:
    script_path = Path(__file__).parent / script_name
    if not script_path.exists():
        print(f"Error: {script_name} not found")
        sys.exit(1)
    try:
        if script_name.endswith('.ps1'):
            # Use PowerShell for .ps1 scripts
            subprocess.run(['powershell', '-ExecutionPolicy', 'Bypass', '-File', str(script_path)], check=True)
        else:
            # Use bash for .sh scripts
            subprocess.run(['bash', str(script_path)], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running setup script: {e}")
        sys.exit(1)
    except FileNotFoundError as e:
        print(f"Error: Required shell not found. {e}")
        sys.exit(1)

def main():
    clear_screen()
    print("Repository Setup Script")
    print("----------------------")
    print("Please select your operating system:")
    print("1. Windows")
    print("2. MacOS")
    print("3. Linux")
    
    while True:
        choice = input("\nEnter your choice (1-3): ").strip()
        
        if choice in ['1', '2', '3']:
            break
        print("Invalid choice. Please try again.")
    
    scripts = {
        '1': 'setup_windows.ps1',
        '2': 'setup_mac.sh',
        '3': 'setup_linux.sh'
    }
    
    script_name = scripts[choice]
    print(f"\nRunning {script_name}...")
    run_setup_script(script_name)
    print("\nSetup complete!")

if __name__ == "__main__":
    main()