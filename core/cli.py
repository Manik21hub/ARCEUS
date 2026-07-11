# core/cli.py
import sys
import os
import argparse
import requests
import subprocess
from tabulate import tabulate

LOCAL_SERVER = "http://127.0.0.1:8443"

def bootstrap_system():
    """Injects the background daemon into Windows Task Scheduler for invisible boot-up."""
    print("[System] Initiating ARCEUS core bootstrap sequence...")
    
    # Locate the background daemon and the windowless python executable
    daemon_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "daemon.py"))
    pythonw_exe = os.path.join(os.path.dirname(os.sys.executable), "pythonw.exe")
    
    # PowerShell command to register a hidden task running at logon
    ps_cmd = f"""
    $action = New-ScheduledTaskAction -Execute '{pythonw_exe}' -Argument '{daemon_path}';
    $trigger = New-ScheduledTaskTrigger -AtLogon;
    $principal = New-ScheduledTaskPrincipal -UserId "$env:USERDOMAIN\\$env:USERNAME" -LogonType Interactive;
    $settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -Hidden;
    Register-ScheduledTask -TaskName "ArceusBackgroundEngine" -Action $action -Trigger $trigger -Principal $principal -Settings $settings -Force;
    Start-ScheduledTask -TaskName "ArceusBackgroundEngine";
    """
    
    subprocess.run(["powershell", "-Command", ps_cmd], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print("[Success] ARCEUS has been permanently integrated into the OS boot sequence.")
    print("The system is now listening in the background.")

def fetch_logs():
    """Pings the invisible background daemon to get the latest chat history."""
    try:
        response = requests.get(f"{LOCAL_SERVER}/api/logs", timeout=2)
        if response.status_code == 200:
            data = response.json()
            table = [[msg['timestamp'], msg['role'], msg['text']] for msg in data.get('history', [])]
            print("\n" + "="*50)
            print("         ARCEUS ACTIVE MEMORY LOGS         ")
            print("="*50)
            print(tabulate(table, headers=["Time", "Entity", "Transmission"]))
            print("="*50 + "\n")
        else:
            print("[Error] Core engine returned an invalid state.")
    except requests.exceptions.ConnectionError:
        print("[Critical] ARCEUS background daemon is currently offline. Restart your PC or run daemon.py manually.")

def shutdown_daemon():
    try:
        requests.post(f"{LOCAL_SERVER}/api/shutdown", timeout=2)
        print("[System] Background daemon terminated gracefully.")
    except:
        print("[System] Daemon was already offline.")

def main():
    parser = argparse.ArgumentParser(description="ARCEUS Desktop AI")
    parser.add_argument('command', nargs='?', default='logs', help='Commands: bootstrap, logs, stop')
    args = parser.parse_args()

    if args.command == 'bootstrap':
        bootstrap_system()
    elif args.command == 'logs':
        fetch_logs()
    elif args.command == 'stop':
        shutdown_daemon()
    else:
        print(f"Unknown command: {args.command}")

if __name__ == "__main__":
    main()