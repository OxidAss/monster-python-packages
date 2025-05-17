import subprocess
import sys
import json
from pathlib import Path

def load_packages(file_path):
    with open(file_path, 'r') as f:
        return [line.strip() for line in f if line.strip() and not line.startswith('#')]

def get_installed_packages():
    result = subprocess.run([sys.executable, '-m', 'pip', 'list', '--format=json'], capture_output=True, text=True)
    if result.returncode != 0:
        print("Failed to get installed packages. Retry if that will 200+ lol.")
        sys.exit(1)
    installed = json.loads(result.stdout)
    return {pkg['name'].lower() for pkg in installed}

def main():
    path = Path('packages.txt')
    if not path.exists():
        print('packages.txt not found. Fuck off.')
        sys.exit(1)

    all_packages = load_packages(path)
    installed = get_installed_packages()
    to_install = [pkg for pkg in all_packages if pkg.lower() not in installed]

    print(f'📦 Total packages listed: {len(all_packages)}')
    print(f'✅ Already installed: {len(all_packages) - len(to_install)}')
    print(f'❌ Missing: {len(to_install)}')

    if not to_install:
        print('All packages are already installed.')
        return

    print('\nPackages to be installed:')
    for pkg in to_install:
        print(f' - {pkg}')

    confirm = input('\nInstall these packages? (y/n): ').strip().lower()
    if confirm != 'y':
        print('Installation aborted.')
        return

    print('\nStarting installation...\n')
    for pkg in to_install:
        print(f'pip install {pkg}')
        subprocess.run([sys.executable, '-m', 'pip', 'install', pkg])

    print('\nAll packages are installed(finally).')

if __name__ == '__main__':
    main()
