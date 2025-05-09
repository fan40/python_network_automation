#!/home/faneva/Bureau/Networking/nenv/bin/python
import paramiko
from dotenv import load_dotenv
import os
import time

load_dotenv()

local_path = "dhcpd.conf"
remote_path = "/etc/dhcp/dhcpd.conf"

USERNAME= os.getenv("USERNAME")
PASSWORD= os.getenv("SERVER")
HOST="192.168.137.14"

client = paramiko.SSHClient()

client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

print(f"Connecting to {HOST}...")

client.connect(hostname=HOST, username=USERNAME, password=PASSWORD)

print("Connected successfully")

sftp = client.open_sftp()

sftp.put(localpath=local_path, remotepath=remote_path)

print("Configuration DHCP términée")

sftp.close()
client.close()