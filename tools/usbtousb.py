import argparse
import subprocess
from datetime import datetime
import os
import sys
import glob
import shutil

CONFIG_FILE = 'USBConfig.txt'

# --- DIRECTORY SETUP ---
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_DIR = os.path.join(SCRIPT_DIR, 'logs')

def get_free_space_gb(path):
    try:
        if not os.path.exists(path): return 0
        stat = os.statvfs(path)
        return (stat.f_frsize * stat.f_bavail) / (1024**3)
    except Exception as e:
        return 0

def setup_config():
    print("--- CONFIGURATION SETUP ---")
    keys = ['source', 'internal_buffer', 'final_dest', 'max_chunk']
    config = load_config(CONFIG_FILE)
    for key in keys:
        if key == 'max_chunk' and 'internal_buffer' in config:
            free = get_free_space_gb(config['internal_buffer'])
            print(f"[INFO] Available space in buffer: {free:.2f} GB")
        current = config.get(key, "")
        new_val = input(f"Enter {key} (Current: {current}): ").strip()
        if new_val:
            config[key] = new_val
    with open(CONFIG_FILE, 'w') as f:
        for k, v in config.items():
            f.write(f"{k}={v}\n")
    print(f"[SUCCESS] Configuration saved to {CONFIG_FILE}")

def load_config(filepath):
    if not os.path.exists(filepath): return {}
    config = {}
    with open(filepath, 'r') as f:
        for line in f:
            if '=' in line:
                key, value = line.strip().split('=', 1)
                config[key.strip()] = value.strip()
    return config

def run_audit(config):
    print("\n--- PRE-FLIGHT AUDIT ---")
    os.makedirs(LOG_DIR, exist_ok=True)
    try:
        lsblk_out = subprocess.check_output(['lsblk', '-f']).decode()
        lsblk_path = os.path.join(LOG_DIR, 'lsblk.txt')
        with open(lsblk_path, 'w') as f:
            f.write(lsblk_out)
        print(f"[OK] Hardware state saved to: {lsblk_path}")
        print(lsblk_out)
    except Exception as e:
        print(f"[ERROR] Could not run lsblk: {e}")

    all_good = True
    for key in ['source', 'final_dest']:
        path = config.get(key)
        if path and os.path.exists(path) and os.access(path, os.W_OK):
            print(f"[OK] {key}: {path} -> Writable")
        else:
            print(f"[!] {key}: {path} -> NOT FOUND or READ-ONLY")
            all_good = False
    print(f"\n[RESULT] {'GOOD' if all_good else 'NO GOOD'}")

def run_transfer(config):
    source = input(f"Source (Keep '{config.get('source', '')}'): ").strip() or config.get('source', '')
    dest = input(f"Destination (Keep '{config.get('final_dest', '')}'): ").strip() or config.get('final_dest', '')
    
    if os.path.exists(source) and os.path.exists(dest):
        if input("Proceed with transfer? (y/n): ").strip().lower() == 'y':
            # Safety First: Explicitly ask to authorize deletion
            mode_prompt = input("Default is COPY. To delete the source type 'delete': ").strip().lower()
            delete_after_copy = (mode_prompt == 'delete')
            
            if delete_after_copy:
                print("[WARNING] Move mode active. Source files will be purged upon success.")
            else:
                print("[INFO] Copy mode active. Source files will be kept safely.")

            os.makedirs(LOG_DIR, exist_ok=True)
            cmd = ['rsync', '-avh', '--progress', '--checksum', '--ignore-existing', f"{source}/", dest]
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                print("\n[VERIFIED] Transfer complete.")
                if delete_after_copy:
                    print("Cleaning source buffer...")
                    try:
                        shutil.rmtree(source)
                        print("[SUCCESS] Source cleared.")
                    except Exception as e:
                        print(f"[!] Warning: Could not delete source buffer: {e}")
                else:
                    print("[SUCCESS] Source untouched (COPY mode).")
            else:
                print("\n[!] Transfer encountered errors. Source files were NOT deleted.")
            with open(os.path.join(LOG_DIR, 'log.txt'), 'w') as f:
                f.write(result.stdout + result.stderr)

def batch_move_folders(config):
    print("\n--- BATCH MOVE SETUP ---")
    src_parent = input(f"Source Parent (Keep '{config.get('source', '')}'): ").strip() or config.get('source', '')
    dst_parent = input(f"Destination Parent (Keep '{config.get('final_dest', '')}'): ").strip() or config.get('final_dest', '')
    
    print("\n[INFO] Running pre-batch audit...")
    if not (os.path.exists(src_parent) and os.path.exists(dst_parent) and os.access(dst_parent, os.W_OK)):
        print("[!] AUDIT FAILED: Source/Destination invalid or not writable.")
        return
    print("[OK] Audit passed. Proceeding...")

    # Handles prefixes, ranges (M-N), or fuzzy matching keywords
    input_val = input("Enter prefix, range (M-N), or keyword (e.g., Song): ").strip()
    
    if '-' in input_val and len(input_val.split('-')) == 2:
        start_char, end_char = input_val.split('-')
        start_char, end_char = start_char.strip(), end_char.strip()
        folders = [f for f in os.listdir(src_parent) 
                   if start_char.lower() <= f[0].lower() <= end_char.lower() 
                   and os.path.isdir(os.path.join(src_parent, f))]
    else:
        # Fuzzy match: catches any folder containing the keyword
        folders = [f for f in os.listdir(src_parent) 
                   if input_val.lower() in f.lower() 
                   and os.path.isdir(os.path.join(src_parent, f))]
    
    if not folders:
        print(f"[!] No folders found matching '{input_val}'")
        return

    # Sort alphabetically for clean logging tracking order
    folders = sorted(folders)

    print(f"\n[INFO] Found {len(folders)} folders.")
    if input(f"Proceed with batch processing for {len(folders)} folders? (y/n): ").strip().lower() == 'y':
        # Safety First: Explicitly ask to authorize deletion for this entire batch
        mode_prompt = input("Default is COPY. To delete the source type 'delete': ").strip().lower()
        delete_after_copy = (mode_prompt == 'delete')
        
        if delete_after_copy:
            print("[WARNING] Delete mode active. Verified folders will be removed from source.")
        else:
            print("[INFO] Copy mode active. All source folders will remain untouched.")

        timestamp_str = datetime.now().strftime('%Y%m%d_%H%M%S')
        log_file = os.path.join(LOG_DIR, f"log_{timestamp_str}.txt")
        report_file = os.path.join(LOG_DIR, f"report_{timestamp_str}.txt")
        
        with open(log_file, 'a') as f: f.write(f"--- STARTING BATCH: {input_val.upper()} ---\n")
        with open(report_file, 'a') as f: f.write(f"--- BATCH SUMMARY: {input_val.upper()} ---\n")

        for folder in folders:
            src, dst = os.path.join(src_parent, folder), os.path.join(dst_parent, folder)
            
            # --- Logging ---
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            with open(log_file, 'a') as f: 
                f.write(f"\n[{timestamp}] [ACTION STARTED] Processing: {folder}\n")
            
            print(f"[ACTION] Processing: {folder}...")
            os.makedirs(dst, exist_ok=True)
            
            cmd = ['rsync', '-avh', '--stats', '--checksum', '--ignore-existing', f"{src}/", dst]
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            # Parse rsync output to separate actual copies from skipped files
            if result.returncode == 0:
                if "Number of regular files transferred: 0" in result.stdout:
                    base_status = "SKIPPED_EXISTING"
                    print(f"[SKIPPED] {folder} already matches destination.")
                else:
                    base_status = "SUCCESS_COPIED"
                    print(f"[VERIFIED] {folder} copied safely.")
                
                # Execute deletion only if 'delete' was typed at the batch prompt
                if delete_after_copy:
                    try:
                        shutil.rmtree(src)
                        status = "SUCCESS_MOVED" if base_status == "SUCCESS_COPIED" else "SKIPPED_AND_DELETED"
                        print(f"[CLEANUP] Source cleared for {folder}.")
                    except Exception as e:
                        status = f"{base_status}_BUT_DELETE_FAILED"
                        print(f"[!] Warning: Could not delete source directory {folder}: {e}")
                else:
                    status = base_status
            else:
                status = "ERROR"
                print(f"[!] Error processing {folder}. Check logs.")
            
            with open(log_file, 'a') as f: 
                f.write(f"[{timestamp}] [STATUS: {status}]\n" + result.stdout + result.stderr)
            with open(report_file, 'a') as f: 
                f.write(f"{folder} -> {status}\n")

def main():
    os.chdir(SCRIPT_DIR)
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--configure', action='store_true')
    parser.add_argument('-i', '--info', action='store_true')
    parser.add_argument('-r', '--run', action='store_true')
    parser.add_argument('-b', '--batch', action='store_true')
    args = parser.parse_args()
    
    if not (args.configure or args.info or args.run or args.batch):
        print("Usage: python3 USBtoUSB.py [-c setup] [-i audit] [-r transfer] [-b batch move]")
        sys.exit(1)

    config = load_config(CONFIG_FILE) if not args.configure else {}
    if args.configure: setup_config()
    elif args.info: run_audit(config)
    elif args.run: run_transfer(config)
    elif args.batch: batch_move_folders(config)

if __name__ == "__main__":
    main()
