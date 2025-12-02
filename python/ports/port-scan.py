import socket

def scan_ports(ip):
    open_ports = []
    for port in range(20, 1024):
        s = socket.socket()
        s.settimeout(1)
        if s.connect_ex((ip, port)) == 0:
            open_ports.append(port)
        s.close()
    return open_ports

print(scan_ports("192.168.1.20"))
