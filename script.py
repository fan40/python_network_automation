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
    if ip in ["192.168.137.6", "192.168.137.7"]:
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

            if ip == "192.168.137.6":
                cmd = [
                "spanning-tree mode pvst",
                "spanning-tree extend system-id",
                "spanning-tree vlan 10 priority 24576",
                "spanning-tree vlan 20 priority 24576",
                "spanning-tree vlan 30 priority 28672",
                "spanning-tree vlan 40 priority 28672"
                    ]
            else:
                cmd = [
                "spanning-tree mode pvst",
                "spanning-tree extend system-id",
                "spanning-tree vlan 30 priority 24576",
                "spanning-tree vlan 40 priority 24576",
                "spanning-tree vlan 10 priority 28672",
                "spanning-tree vlan 20 priority 28672"
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

