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
    if ip in ["192.168.137.12", "192.168.137.13", "192.168.137.14"]:
        print(f"{ip} doesnt belong to the configuration")
    else:
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


            hostname = net_conn.send_command("show running-config | include hostname")
            output = net_conn.send_command("terminal length 0")
            print(output)

            backup = net_conn.send_command("show run")
            time.sleep(2)

            print(backup)

            with open(f"config_equipement/{hostname.split()[1]}.backup", "w") as file:
                file.write(backup)
            
            print(f"Backup {hostname.split()[1]} fait.")


            net_conn.disconnect()
        except NetMikoAuthenticationException:
            print(f"Failed to authenticate")
        except NetMikoTimeoutException:
            print("Host unreachable")