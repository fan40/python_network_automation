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
    try:
        if ip in ["192.168.137.6", "192.168.137.7"]:
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

            print("Connected successfullly")

            cmd = [
                "int range g0/0-3, g1/0",
                "switchport trunk enc dot1Q",
                "switchport mode trunk",
                "switchport trunk allowed vlan 10,20,30,40,99",
                "end",
                "write memory"
            ]


            output = net_conn.send_config_set(cmd)
            time.sleep(1)
            print(output)

            net_conn.disconnect()
        else:
            print(f"{ip} not belongs to the configuration")
    except NetMikoAuthenticationException:
        print(f"Failed to authenticate to {ip}")
    except NetMikoTimeoutException:
        print(f"Host unreachable")