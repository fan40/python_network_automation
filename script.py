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
    if ip in ["192.168.137.4", "192.168.137.5"]:
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

            if ip == "192.168.137.4":
                cmd = [
                    "int f0/0.10",
                    "encapsulation dot1Q 10",
                    "ip add 192.168.10.2 255.255.255.0",
                    "ip helper-address 172.16.10.5",
                    "no sh",
                    "standby 10 ip 192.168.10.1",
                    "standby 10 priority 110",
                    "standby 10 preempt",
                    "exit",
                    "int f0/0.20",
                    "encapsulation dot1Q 20",
                    "ip add 192.168.20.2 255.255.255.0",
                    "ip helper-address 172.16.10.5",
                    "no sh",
                    "standby 20 ip 192.168.20.1",
                    "standby 20 priority 110",
                    "standby 20 preempt",
                    "exit",
                    "int f0/0.30",
                    "encapsulation dot1Q 30",
                    "ip add 192.168.30.2 255.255.255.0",
                    "ip helper-address 172.16.10.5",
                    "no sh",
                    "standby 30 ip 192.168.30.1",
                    "standby 30 preempt",
                    "exit",
                    "int f0/0.40",
                    "encapsulation dot1Q 40",
                    "ip add 192.168.40.2 255.255.255.0",
                    "ip helper-address 172.16.10.5",
                    "no sh",
                    "standby 40 ip 192.168.40.1",
                    "standby 40 preempt",
                    "end",
                    "wr mem"
                ]
            else:
                cmd = [
                    "int f0/0.10",
                    "encapsulation dot1Q 10",
                    "ip add 192.168.10.3 255.255.255.0",
                    "ip helper-address 172.16.10.5",
                    "no sh",
                    "standby 10 ip 192.168.10.1",
                    "standby 10 preempt",
                    "exit",
                    "int f0/0.20",
                    "encapsulation dot1Q 20",
                    "ip add 192.168.20.3 255.255.255.0",
                    "ip helper-address 172.16.10.5",
                    "no sh",
                    "standby 20 ip 192.168.20.1",
                    "standby 20 preempt",
                    "exit",
                    "int f0/0.30",
                    "encapsulation dot1Q 30",
                    "ip add 192.168.30.3 255.255.255.0",
                    "ip helper-address 172.16.10.5",
                    "no sh",
                    "standby 30 ip 192.168.30.1",
                    "standby 30 priority 110",
                    "standby 30 preempt",
                    "exit",
                    "int f0/0.40",
                    "encapsulation dot1Q 40",
                    "ip add 192.168.40.3 255.255.255.0",
                    "ip helper-address 172.16.10.5",
                    "no sh",
                    "standby 40 ip 192.168.40.1",
                    "standby 40 priority 110",
                    "standby 40 preempt",
                    "end",
                    "wr mem"
                ]

            output = net_conn.send_config_set(cmd)
            time.sleep(3)
            print(output)

            net_conn.disconnect()
        except NetMikoAuthenticationException:
            print(f"Failed to authenticate")
        except NetMikoTimeoutException:
            print("Host unreachable")
    else:
        print(f"{ip} is not belongs the configuration")

