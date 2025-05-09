#!/home/faneva/Bureau/Networking/nenv/bin/python



from dotenv import load_dotenv
from netmiko import ConnectHandler, NetMikoAuthenticationException, NetMikoTimeoutException
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
            "host":ip,
            "username":USERNAME,
            "password":PASSWORD,
            "secret":SECRET
        }
        if ip in ["192.168.137.6", "192.168.137.7"]:
            print(f"Connecting to {ip}...")
            net_con = ConnectHandler(**device)

            print("Connected successfully")
            net_con.enable()

            cmd = [
                "int range g1/2-3",
                "channel-proto lacp",
                "channel-group 1 mode active",
                "exit",
                "int port-channel 1",
                "switchport trunk enc dot1",
                "switchport mode trunk",
                "switchport trunk allowed vlan 10,20,30,40,99",
                "end"
            ]

            output = net_con.send_config_set(cmd)

            time.sleep(1)

            print(output)

            net_con.disconnect()
        else:
            print(f"{ip} non configurable en etherchannel")

    except NetMikoAuthenticationException:
        print(f"Failed to authenticate to the host {ip}")
    except NetMikoTimeoutException:
        print(f"Host unreachable")