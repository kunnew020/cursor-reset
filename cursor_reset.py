#!/usr/bin/env python3
"""
Cursor Trial Reset Script for macOS
Resets Cursor trial by generating new machine IDs and patching application files.
"""

import os
import sys
import json
import uuid
import hashlib
import shutil
import sqlite3
import tempfile
import re
from pathlib import Path

# ANSI color codes for terminal output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    CYAN = '\033[96m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def print_info(msg):
    print(f"{Colors.CYAN}ℹ️  {msg}{Colors.RESET}")

def print_success(msg):
    print(f"{Colors.GREEN}✅ {msg}{Colors.RESET}")

def print_error(msg):
    print(f"{Colors.RED}❌ {msg}{Colors.RESET}")

def print_warning(msg):
    print(f"{Colors.YELLOW}⚠️  {msg}{Colors.RESET}")

def check_macos():
    """Ensure script is running on macOS"""
    if sys.platform != "darwin":
        print_error("This script only works on macOS!")
        sys.exit(1)

def get_cursor_paths():
    """Get Cursor application paths"""
    paths = {
        'app_path': '/Applications/Cursor.app/Contents/Resources/app',
        'storage_json': os.path.expanduser('~/Library/Application Support/Cursor/User/globalStorage/storage.json'),
        'state_db': os.path.expanduser('~/Library/Application Support/Cursor/User/globalStorage/state.vscdb'),
        'machine_id': os.path.expanduser('~/Library/Application Support/Cursor/machineId'),
        'package_json': '/Applications/Cursor.app/Contents/Resources/app/package.json',
        'main_js': '/Applications/Cursor.app/Contents/Resources/app/out/main.js',
        'workbench_js': '/Applications/Cursor.app/Contents/Resources/app/out/vs/workbench/workbench.desktop.main.js'
    }
    return paths

def check_cursor_installed(paths):
    """Check if Cursor is installed"""
    if not os.path.exists(paths['app_path']):
        print_error("Cursor is not installed at /Applications/Cursor.app")
        print_info("Please install Cursor first: https://cursor.sh")
        sys.exit(1)
    print_success("Cursor installation found")

def check_cursor_running():
    """Check if Cursor is running and warn user"""
    import subprocess
    result = subprocess.run(['pgrep', '-x', 'Cursor'], capture_output=True)
    if result.returncode == 0:
        print_warning("Cursor is currently running!")
        print_info("It's recommended to quit Cursor before continuing.")
    else:
        print_success("Cursor is not running")

def generate_new_ids():
    """Generate new machine IDs"""
    print_info("Generating new machine IDs...")
    
    dev_device_id = str(uuid.uuid4())
    machine_id = hashlib.sha256(os.urandom(32)).hexdigest()
    mac_machine_id = hashlib.sha512(os.urandom(64)).hexdigest()
    sqm_id = "{" + str(uuid.uuid4()).upper() + "}"
    
    new_ids = {
        "telemetry.devDeviceId": dev_device_id,
        "telemetry.macMachineId": mac_machine_id,
        "telemetry.machineId": machine_id,
        "telemetry.sqmId": sqm_id,
        "storage.serviceMachineId": dev_device_id
    }
    
    print_success("New machine IDs generated")
    return new_ids, dev_device_id

def backup_file(file_path):
    """Create backup of a file"""
    if os.path.exists(file_path):
        backup_path = f"{file_path}.backup"
        shutil.copy2(file_path, backup_path)
        print_info(f"Backed up: {os.path.basename(file_path)}")
        return backup_path
    return None

def update_storage_json(storage_path, new_ids):
    """Update storage.json with new machine IDs"""
    print_info("Updating storage.json...")
    
    if not os.path.exists(storage_path):
        print_warning(f"storage.json not found at {storage_path}")
        return False
    
    backup_file(storage_path)
    
    try:
        with open(storage_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        config.update(new_ids)
        
        with open(storage_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=4)
        
        print_success("storage.json updated")
        return True
    except Exception as e:
        print_error(f"Failed to update storage.json: {e}")
        return False

def update_state_db(db_path, new_ids):
    """Update state.vscdb SQLite database"""
    print_info("Updating state database...")
    
    if not os.path.exists(db_path):
        print_warning(f"state.vscdb not found at {db_path}")
        return False
    
    backup_file(db_path)
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ItemTable (
                key TEXT PRIMARY KEY,
                value TEXT
            )
        """)
        
        for key, value in new_ids.items():
            cursor.execute("""
                INSERT OR REPLACE INTO ItemTable (key, value) 
                VALUES (?, ?)
            """, (key, value))
        
        conn.commit()
        conn.close()
        
        print_success("State database updated")
        return True
    except Exception as e:
        print_error(f"Failed to update state database: {e}")
        return False

def update_machine_id_file(machine_id_path, dev_device_id):
    """Update machineId file"""
    print_info("Updating machineId file...")
    
    machine_id_dir = os.path.dirname(machine_id_path)
    if not os.path.exists(machine_id_dir):
        os.makedirs(machine_id_dir, exist_ok=True)
    
    if os.path.exists(machine_id_path):
        backup_file(machine_id_path)
    
    try:
        with open(machine_id_path, 'w') as f:
            f.write(dev_device_id)
        
        print_success("machineId file updated")
        return True
    except Exception as e:
        print_error(f"Failed to update machineId: {e}")
        return False

def patch_main_js(main_path):
    """Patch main.js to bypass machine ID checks"""
    print_info("Patching main.js...")
    
    if not os.path.exists(main_path):
        print_warning(f"main.js not found at {main_path}")
        return False
    
    backup_file(main_path)
    
    try:
        # Preserve file permissions
        original_stat = os.stat(main_path)
        original_mode = original_stat.st_mode
        
        with open(main_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Patch getMachineId and getMacMachineId functions
        patterns = {
            r"async getMachineId\(\)\{return [^??]+\?\?([^}]+)\}": r"async getMachineId(){return \1}",
            r"async getMacMachineId\(\)\{return [^??]+\?\?([^}]+)\}": r"async getMacMachineId(){return \1}",
        }
        
        modified = False
        for pattern, replacement in patterns.items():
            new_content = re.sub(pattern, replacement, content)
            if new_content != content:
                content = new_content
                modified = True
        
        if modified:
            with tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='utf-8') as tmp_file:
                tmp_file.write(content)
                tmp_path = tmp_file.name
            
            shutil.move(tmp_path, main_path)
            os.chmod(main_path, original_mode)
            
            print_success("main.js patched")
        else:
            print_info("main.js already patched or pattern not found")
        
        return True
    except Exception as e:
        print_error(f"Failed to patch main.js: {e}")
        return False

def patch_workbench_js(workbench_path):
    """Patch workbench.desktop.main.js (backup only, no modifications)"""
    print_info("Creating backup of workbench.desktop.main.js...")
    
    if not os.path.exists(workbench_path):
        print_warning(f"workbench.desktop.main.js not found at {workbench_path}")
        return False
    
    backup_file(workbench_path)
    
    # No UI modifications - just backup for safety
    print_success("workbench.desktop.main.js backed up (no modifications)")
    return True

def main():
    """Main function"""
    print(f"\n{Colors.BOLD}{Colors.CYAN}========================================")
    print("  Cursor Trial Reset Script for macOS")
    print(f"========================================{Colors.RESET}\n")
    
    # Check if running on macOS
    check_macos()
    
    # Get paths
    paths = get_cursor_paths()
    
    # Check Cursor installation
    check_cursor_installed(paths)
    
    # Check if Cursor is running
    check_cursor_running()
    
    # Confirm action
    print_warning("This script will:")
    print("  • Generate new machine IDs")
    print("  • Modify Cursor configuration files (storage.json, state.vscdb, machineId)")
    print("  • Patch main.js to bypass machine ID checks")
    print("  • Backup original files (.backup)")
    print("  • NO UI modifications - Cursor appearance unchanged")
    print()
    response = input(f"{Colors.YELLOW}Continue? (y/N): {Colors.RESET}")
    if response.lower() != 'y':
        print_info("Operation cancelled")
        sys.exit(0)
    
    print()
    print_info("Starting Cursor trial reset...\n")
    
    # Generate new IDs
    new_ids, dev_device_id = generate_new_ids()
    
    # Update storage files
    update_storage_json(paths['storage_json'], new_ids)
    update_state_db(paths['state_db'], new_ids)
    update_machine_id_file(paths['machine_id'], dev_device_id)
    
    # Patch application files
    patch_main_js(paths['main_js'])
    patch_workbench_js(paths['workbench_js'])
    
    print()
    print_success(f"{Colors.BOLD}Cursor trial reset complete!{Colors.RESET}")
    print_info("Please restart Cursor for changes to take effect.")
    print()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Operation cancelled by user{Colors.RESET}")
        sys.exit(0)
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
