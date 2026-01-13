"""
Auto Open HMOPI ORS Tunnel
Location: C:\1jap\Automation\AutoOpenHmopiorsTunnel.py
This script automatically starts all servers and exposes them through Cloudflare tunnel
"""

import subprocess
import time
import os
import sys

# ============== CONFIGURATION ==============
BACKEND_PATH = r"C:\xampp\htdocs\Online-Registration-System-Deployment\backend"
FRONTEND_PATH = r"C:\xampp\htdocs\Online-Registration-System-Deployment\frontend"
CLOUDFLARED_CONFIG = r"C:\Users\MIS jap\.cloudflared\config.yml"
TUNNEL_NAME = "hmopiors"

# Commands
BACKEND_CMD = "php artisan serve --port=8000 --host=0.0.0.0", "php artisan queue:work"
FRONTEND_CMD = "npx serve -s dist -l 5173"
TUNNEL_CMD = f'cloudflared tunnel --config "{CLOUDFLARED_CONFIG}" run {TUNNEL_NAME}'

# ============== COLORS FOR CONSOLE ==============
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'

def print_banner():
    """Print startup banner"""
    os.system('cls' if os.name == 'nt' else 'clear')
    banner = """
    ╔═══════════════════════════════════════════════════════════════╗
    ║                                                               ║
    ║     🚀 HMOPI ORS TUNNEL AUTO-STARTER 🚀                      ║
    ║                                                               ║
    ║     Backend  : Laravel (Port 8000)                           ║
    ║     Frontend : Vite/Serve (Port 5173)                        ║
    ║     Tunnel   : Cloudflared (hmopiors)                        ║
    ║                                                               ║
    ╚═══════════════════════════════════════════════════════════════╝
    """
    print(Colors.CYAN + banner + Colors.END)

def check_path_exists(path, name):
    """Check if the required path exists"""
    if not os.path.exists(path):
        print(f"{Colors.FAIL}[ERROR] {name} path not found: {path}{Colors.END}")
        return False
    print(f"{Colors.GREEN}[OK] {name} path verified: {path}{Colors.END}")
    return True

def start_backend():
    """Start Laravel backend server"""
    print(f"\n{Colors.BLUE}[1/3] Starting Backend Server...{Colors.END}")
    print(f"      Path: {BACKEND_PATH}")
    print(f"      Command: {BACKEND_CMD}")
    
    # Open new CMD window for backend
    cmd = f'start "HMOPI Backend - Port 8000" cmd /k "cd /d {BACKEND_PATH} && {BACKEND_CMD}"'
    subprocess.Popen(cmd, shell=True)
    
    print(f"{Colors.GREEN}      ✓ Backend server starting...{Colors.END}")
    time.sleep(2)

def start_frontend():
    """Start Frontend server"""
    print(f"\n{Colors.BLUE}[2/3] Starting Frontend Server...{Colors.END}")
    print(f"      Path: {FRONTEND_PATH}")
    print(f"      Command: {FRONTEND_CMD}")
    
    # Open new CMD window for frontend
    cmd = f'start "HMOPI Frontend - Port 5173" cmd /k "cd /d {FRONTEND_PATH} && {FRONTEND_CMD}"'
    subprocess.Popen(cmd, shell=True)
    
    print(f"{Colors.GREEN}      ✓ Frontend server starting...{Colors.END}")
    time.sleep(2)

def start_tunnel():
    """Start Cloudflare tunnel"""
    print(f"\n{Colors.BLUE}[3/3] Starting Cloudflare Tunnel...{Colors.END}")
    print(f"      Config: {CLOUDFLARED_CONFIG}")
    print(f"      Tunnel: {TUNNEL_NAME}")
    
    # Open new CMD window for tunnel
    cmd = f'start "HMOPI Cloudflare Tunnel" cmd /k "{TUNNEL_CMD}"'
    subprocess.Popen(cmd, shell=True)
    
    print(f"{Colors.GREEN}      ✓ Cloudflare tunnel starting...{Colors.END}")

def print_summary():
    """Print summary of running services"""
    summary = f"""
    {Colors.GREEN}
    ╔═══════════════════════════════════════════════════════════════╗
    ║                    ALL SERVICES STARTED!                      ║
    ╠═══════════════════════════════════════════════════════════════╣
    ║                                                               ║
    ║  📦 Backend Server:                                          ║
    ║     └─ http://localhost:8000                                 ║
    ║     └─ http://0.0.0.0:8000                                   ║
    ║                                                               ║
    ║  🌐 Frontend Server:                                         ║
    ║     └─ http://localhost:5173                                 ║
    ║                                                               ║
    ║  🔒 Cloudflare Tunnel:                                       ║
    ║     └─ Tunnel Name: {TUNNEL_NAME}                               ║
    ║     └─ Check your Cloudflare dashboard for URLs              ║
    ║                                                               ║
    ╠═══════════════════════════════════════════════════════════════╣
    ║                                                               ║
    ║  ⚠️  DO NOT CLOSE THIS WINDOW OR THE CMD WINDOWS!            ║
    ║                                                               ║
    ║  To stop all services:                                       ║
    ║  1. Close each CMD window manually, OR                       ║
    ║  2. Press Ctrl+C in each window                              ║
    ║                                                               ║
    ╚═══════════════════════════════════════════════════════════════╝
    {Colors.END}
    """
    print(summary)

def main():
    """Main function to run all services"""
    print_banner()
    
    # Verify paths exist
    print(f"{Colors.WARNING}Verifying paths...{Colors.END}\n")
    
    paths_valid = True
    if not check_path_exists(BACKEND_PATH, "Backend"):
        paths_valid = False
    if not check_path_exists(FRONTEND_PATH, "Frontend"):
        paths_valid = False
    if not check_path_exists(CLOUDFLARED_CONFIG, "Cloudflared Config"):
        paths_valid = False
    
    if not paths_valid:
        print(f"\n{Colors.FAIL}[ERROR] Some paths are invalid. Please check the configuration.{Colors.END}")
        input("\nPress Enter to exit...")
        sys.exit(1)
    
    print(f"\n{Colors.GREEN}All paths verified successfully!{Colors.END}")
    print(f"\n{Colors.WARNING}Starting all services...{Colors.END}")
    
    # Start all services
    start_backend()
    start_frontend()
    start_tunnel()
    
    # Print summary
    print_summary()
    
    # Keep the script running
    input("\nPress Enter to exit this window (services will keep running)...")

if __name__ == "__main__":
    main()