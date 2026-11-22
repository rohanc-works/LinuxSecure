#!/usr/bin/env python3
import subprocess
import sys
import os

def run(cmd):
    subprocess.run(cmd, shell=True, check=True)

def install_if_missing(package):
    try:
        __import__(package)
    except ImportError:
        run(f"pip install {package}")

install_if_missing("psutil")
install_if_missing("requests")

def harden_ssh():
    ssh_config = "/etc/ssh/sshd_config"
    if os.path.exists(ssh_config):
        with open(ssh_config, "r") as f:
            content = f.read()
        
        changes = {
            "#PermitRootLogin prohibit-password": "PermitRootLogin no",
            "#PasswordAuthentication yes": "PasswordAuthentication no",
            "PermitRootLogin yes": "PermitRootLogin no",
            "PasswordAuthentication yes": "PasswordAuthentication no"
        }
        
        for old, new in changes.items():
            content = content.replace(old, new)
            
        with open(ssh_config, "w") as f:
            f.write(content)
        run("systemctl restart sshd")

def setup_ufw():
    run("ufw default deny incoming")
    run("ufw default allow outgoing")
    run("ufw allow ssh")
    run("yes | ufw enable")

def setup_fail2ban():
    jail_local = "/etc/fail2ban/jail.local"
    config = """[sshd]
enabled = true
port = ssh
filter = sshd
logpath = /var/log/auth.log
maxretry = 3
bantime = 3600"""
    with open(jail_local, "w") as f:
        f.write(config)
    run("systemctl restart fail2ban")

def enable_auto_updates():
    run("apt-get install -y unattended-upgrades")
    run("dpkg-reconfigure -f noninteractive unattended-upgrades")

if __name__ == "__main__":
    if os.geteuid() != 0:
        print("Run as root")
        sys.exit(1)
    
    run("apt-get update -qq")
    harden_ssh()
    setup_ufw()
    setup_fail2ban()
    enable_auto_updates()
    print("Done")
