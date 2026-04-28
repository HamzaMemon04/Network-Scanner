# Network Scanner

This is my second cybersecurity-related project.
It is a Python-based tool that scans a target network, discovers live hosts, finds open ports, and identifies running services — then generates a detailed HTML report.

# Features
Discovers live hosts on a network range
Scans top 1000 most common TCP ports
Detects:
Open ports
Running services
Software versions
Classifies findings by risk level:
HIGH → MEDIUM → LOW
Automatically flags risky ports:
445 (SMB), 3389 (RDP), 22 (SSH), 21 (FTP), 23 (Telnet), 3306 (MySQL)
Generates a dark-themed HTML report
Skips unresponsive hosts (timeout handling)
🛠️ Tech Used
Python 3.x
Nmap
python-nmap library

# How It Works

The scanner works in three phases:

Phase 1 — Host Discovery:- Scans the network range to find live devices./n
Phase 2 — Port Scanning:- Scans top 1000 ports on each host. Identifies port states (open / closed / filtered).
Phase 3 — Report Generation:- Generates a structured HTML report with risk levels.

# How To Run
Run the script: python scanner.py 192.168.0.0/24
To find your network range: Run ipconfig (Windows)
Check your IPv4 address
Example: IP: 192.168.1.45 → Range: 192.168.1.0/24

# Note
This tool is for educational purposes only
Only scan networks you own or have permission to test
Unauthorized scanning is illegal

# What I Learned
How network scanning works
Host discovery using ping sweeps
Port states: open, closed, filtered
Basics of TCP handshake in scanning
Service detection and fingerprinting
High-risk ports in cybersecurity
Python scripting and automation
Working with Nmap using python-nmap
Understanding CIDR and network ranges

# Future Improvements
Add UDP port scanning
Add CVE lookup for detected services
Add JSON report export
Build GUI version
Add OS detection

# Author
Hamza
