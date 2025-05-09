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

        output = net_conn.send_command("show run | include hostname")
        print(output)

        net_conn.disconnect()
    except NetMikoAuthenticationException:
        print(f"Failed to authenticate")
    except NetMikoTimeoutException:
        print("Host unreachable")

