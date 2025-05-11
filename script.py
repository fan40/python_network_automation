#!/home/faneva/Bureau/Networking/nenv/bin/python

from netmiko import ConnectHandler, NetMikoAuthenticationException, NetMikoTimeoutException
import time
from dotenv import load_dotenv
import os

load_dotenv()

USERNAME = os.getenv("NET_USER")
PASSWORD = os.getenv("NET_PASSWORD")
SECRET = os.getenv("NET_SECRET")

with open("ips.txt", "r") as file:
    ips = [ip.strip() for ip in file.readlines()]

for ip in ips:
    if ip in ["192.168.137.8", "192.168.137.9", "192.168.137.10", "192.168.137.11"]:
        try:
            device = {
                "device_type":"cisco_ios",
                "host":ip,
                "username":USERNAME,
                "password":PASSWORD,
                "secret":SECRET
            }

            print(f"Connecting to {ip}...")
            net_conn = ConnectHandler(**device)
            net_conn.enable()
            print("Connected successfully")

            cmd = [
                "interface e0/2",
                "switchport mode access",
                "switchport access vlan 10",
                "exit",
                "interface e0/3",
                "switchport mode access",
                "switchport access vlan 20",
                "exit",
                "interface e1/0",
                "switchport mode access",
                "switchport access vlan 30",
                "exit",
                "interface e1/1",
                "switchport mode access",
                "switchport access vlan 40",
                "end"
            ]

            output = net_conn.send_config_set(cmd)
            time.sleep(1)
            print(output)

            net_conn.disconnect()
        except NetMikoAuthenticationException:
            print(f"Failed to authenticate")
        except NetMikoTimeoutException:
            print("Host unreachable")
    else:
        print(f"{ip} dont belongs to the configuration")