"""
Auto Open HMOPI ORS Tunnel - Multi-Environment Version
Location: C:\\1jap\\Automation\\AutoOpenHmopiorsTunnel.py
"""

import subprocess
import time
import os
import argparse
import shutil

# ============== ARGUMENT PARSING ==============
parser = argparse.ArgumentParser(description='Start HMOPI ORS servers')
parser.add_argument('--env', default='development', choices=['development', 'staging', 'production'],
                   help='Environment to start (default: development)')
args = parser.parse_args()
ENVIRONMENT = args.env

# ============== CONFIGURATION ==============
BASE_PATH = r"C:\xampp\htdocs\Online-Registration-System-Deployment"
BACKEND_PATH = os.path.join(BASE_PATH, "backend")
FRONTEND_PATH = os.path.join(BASE_PATH, "frontend")
CLOUDFLARED_CONFIG = r"C:\Users\MIS jap\.cloudflared\config.yml"

# Environment-specific configurations
configs = {
    'development': {
        'backend_port': 8000,
        'frontend_port': 5173,
        'tunnel_name': 'hmopiors',
        'backend_env_file': '.env.development',
        'start_tunnel': True,
        'frontend_cmd': f"npm run dev -- --port 5173"
    },
    'staging': {
        # CRITICAL FIX: Must match config.yml ports (8000/5173)
        'backend_port': 8000,      
        'frontend_port': 5173,     
        'tunnel_name': 'hmopiors',
        'backend_env_file': '.env.staging',
        'start_tunnel': True,
        # CRITICAL FIX: Serve the BUILD folder for Staging (like your old script)
        'frontend_cmd': "npx serve -s dist -l 5173"     
    },
    'production': {
        'backend_port': 8000,
        'frontend_port': 5173,
        'tunnel_name': 'hmopiors',
        'backend_env_file': '.env.production',
        'start_tunnel': True,
        'frontend_cmd': "npx serve -s dist -l 5173"
    }
}

config = configs[ENVIRONMENT]

# Commands
# Backend listens on 0.0.0.0 so Cloudflare can find it
BACKEND_CMD = f"php artisan serve --port={config['backend_port']} --host=0.0.0.0"
FRONTEND_CMD = config['frontend_cmd']
TUNNEL_CMD = f'cloudflared tunnel --config "{CLOUDFLARED_CONFIG}" run {config["tunnel_name"]}'

# ============== COLORS ==============
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    END = '\033[0m'

def print_banner():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(Colors.HEADER + f"""
    🚀 HMOPI ORS STARTUP: {ENVIRONMENT.upper()}
    =========================================
    Backend Port  : {config['backend_port']}
    Frontend Port : {config['frontend_port']}
    Database Env  : {config['backend_env_file']}
    Tunnel Name   : {config['tunnel_name']}
    =========================================
    """ + Colors.END)

def setup_environment():
    """Switches the .env file in the backend and clears cache"""
    print(f"{Colors.BLUE}[Config] Setting up {ENVIRONMENT} environment...{Colors.END}")
    
    source = os.path.join(BACKEND_PATH, config['backend_env_file'])
    destination = os.path.join(BACKEND_PATH, '.env')
    
    if os.path.exists(source):
        try:
            # 1. Copy file
            shutil.copyfile(source, destination)
            print(f"{Colors.GREEN}  ✓ Copied {config['backend_env_file']} to .env{Colors.END}")
            
            # 2. CLEAR CACHE
            print(f"{Colors.BLUE}  > Clearing Laravel Config Cache...{Colors.END}")
            subprocess.run(f'cd /d "{BACKEND_PATH}" && php artisan config:clear', shell=True, check=True, stdout=subprocess.DEVNULL)
            print(f"{Colors.GREEN}  ✓ Cache Cleared Successfully{Colors.END}")
            
        except Exception as e:
            print(f"{Colors.FAIL}  ✗ Error setting up env: {e}{Colors.END}")
    else:
        print(f"{Colors.FAIL}  ✗ Source file {config['backend_env_file']} not found!{Colors.END}")

def start_services():
    # 1. Start Backend
    print(f"\n{Colors.BLUE}[1/3] Starting Backend (Port: {config['backend_port']})...{Colors.END}")
    cmd_backend = f'start "Backend ({ENVIRONMENT})" cmd /k "cd /d "{BACKEND_PATH}" && {BACKEND_CMD}"'
    subprocess.Popen(cmd_backend, shell=True)
    time.sleep(2)

    # 2. Start Frontend
    print(f"{Colors.BLUE}[2/3] Starting Frontend (Port: {config['frontend_port']})...{Colors.END}")
    cmd_frontend = f'start "Frontend ({ENVIRONMENT})" cmd /k "cd /d "{FRONTEND_PATH}" && {FRONTEND_CMD}"'
    subprocess.Popen(cmd_frontend, shell=True)
    time.sleep(2)

    # 3. Start Tunnel (if enabled)
    if config['start_tunnel']:
        print(f"{Colors.BLUE}[3/3] Starting Tunnel...{Colors.END}")
        cmd_tunnel = f'start "Cloudflare Tunnel" cmd /k "{TUNNEL_CMD}"'
        subprocess.Popen(cmd_tunnel, shell=True)
    else:
        print(f"{Colors.WARNING}[3/3] Tunnel skipped for this environment.{Colors.END}")

if __name__ == "__main__":
    print_banner()
    setup_environment()
    start_services()
    print(f"\n{Colors.GREEN}✔ All services requested.{Colors.END}")