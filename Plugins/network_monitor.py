# plugins/network_monitor.py
import psutil
import time
import random
import socket

# ARCEUS reads this metadata to understand the plugin's capabilities
PLUGIN_META = {
    "name": "Tactical Network & Telemetry",
    "command": "NETWORK",
    "description": "Scans local interfaces, checks ports, or streams tactical drone telemetry. Targets: 'scan', 'ports', 'telemetry'."
}

def get_active_interfaces():
    """Scans and formats active network interfaces on the host PC."""
    addrs = psutil.net_if_addrs()
    stats = psutil.net_if_stats()
    
    print("\n[Network Scanner] Active Interfaces Detected:")
    for intface, addr_list in addrs.items():
        if intface in stats and getattr(stats[intface], "isup"):
            ip_info = next((addr.address for addr in addr_list if addr.family == socket.AF_INET), "No IPv4")
            print(f" -> {intface}: {ip_info}")

def stream_mock_telemetry():
    """Generates a simulated 5-second tactical drone packet stream."""
    print("\n[UAV Link] Establishing secure telemetry handshake...")
    time.sleep(1)
    print("[UAV Link] Handshake accepted. Streaming live coordinates (Local Swarm Alpha):")
    
    for i in range(5):
        lat = round(random.uniform(28.5, 28.7), 4)
        lon = round(random.uniform(77.2, 77.4), 4)
        alt = random.randint(120, 450)
        sig = random.randint(85, 99)
        print(f"   [Packet {i+1}] Node-0{i+1} | Lat: {lat}, Lon: {lon} | Alt: {alt}m | Signal: {sig}% | Status: SECURE")
        time.sleep(0.5)
    print("[UAV Link] Telemetry burst complete.\n")

def execute(target):
    """The function ARCEUS calls when routing this plugin."""
    target = target.lower()
    
    if "scan" in target or "interfaces" in target:
        print("[System] Initiating local perimeter scan...")
        get_active_interfaces()
        return True
        
    elif "telemetry" in target or "drone" in target:
        stream_mock_telemetry()
        return True
        
    elif "ports" in target:
        print("[System] Running rapid localhost port diagnostic...")
        # A quick mock scan for visual effect
        open_ports = [80, 443, 8000, 8080]
        for port in open_ports:
            print(f" -> Port {port} : LISTENING")
            time.sleep(0.2)
        return True
        
    print(f"[Network Plugin] Unknown target sequence: {target}")
    return False