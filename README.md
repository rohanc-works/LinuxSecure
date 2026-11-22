# LinuxSecure

A simple script to secure a new Ubuntu server.

## What it does

It updates the system and installs basic security tools. It turns on the firewall, stops root login over SSH, and blocks people who try to guess your password. It also makes sure the server updates itself automatically.

## How to use

1. Clone this repository.
2. Run the script with sudo.

```bash
sudo python3 linux_secure.py
```

## Important

Make sure you can log in with an SSH key before you run this. The script will turn off password login. If you do not have a key set up, you might lock yourself out of the server.