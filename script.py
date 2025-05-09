#!/home/faneva/Bureau/Networking/nenv/bin/python

from netmiko import ConnectHandler, NetMikoAuthenticationException, NetMikoTimeoutException
from dotenv import load_dotenv
import time
import os

load_dotenv()

USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")
SECRET = os.getenv("SECRET")

with open("ips.txt", "r") as file:
    ips = [ip.strip() for ip in file.readlines()]

for ip in ips:
    if ip in ["192.168.137.8", "192.168.137.9", "192.168.137.10", "192.168.137.11"]:
        try:
            device = {
                "device_type":"cisco_ios",
                "host": ip,
                "username": USERNAME,
                "password": PASSWORD,
                "secret": SECRET
            }

            print(f"Connecting to {ip}...")
            net_conn = ConnectHandler(**device)
            net_conn.enable()
            print("Connected successfully")

            cmd = [
                "interface range e0/0-1",
                "switchport trunk enc dot1Q",
                "switchport mode trunk",
                "switchport trunk allowed vlan 10,20,30,40,99",
                "end",
                "wr mem"
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
        print(f"{ip} is not belongs the configuration")

