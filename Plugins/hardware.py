# plugins/hardware.py
import psutil

# ARCEUS uses this dictionary to understand how and when to use this script
PLUGIN_META = {
    "name": "Hardware Telemetry",
    "command": "SYSSTATS",
    "description": "Reads PC hardware data. Target can be 'cpu', 'ram', or 'battery'."
}

def execute(target):
    """The function ARCEUS calls when this plugin is triggered."""
    if "cpu" in target:
        cpu_usage = psutil.cpu_percent(interval=1)
        print(f"[Hardware Plugin] CPU Load is at {cpu_usage}%")
        return True
    
    elif "ram" in target:
        ram = psutil.virtual_memory()
        print(f"[Hardware Plugin] Memory usage is {ram.percent}%")
        return True
        
    elif "battery" in target:
        if not hasattr(psutil, "sensors_battery"):
            print("[Hardware Plugin] No battery hardware detected.")
            return True
            
        battery = psutil.sensors_battery()
        if battery:
            plugged = "Plugged In" if battery.power_plugged else "Discharging"
            print(f"[Hardware Plugin] Battery is at {battery.percent}% ({plugged})")
        return True
        
    print(f"[Hardware Plugin] Unknown target metric: {target}")
    return False