# Network-Scanner

This is my second cybersecurity-related project.
It is a Python-based tool that scans a target network, discovers live hosts, finds open ports, and identifies running services — then generates a detailed HTML report.
Features

Discovers live hosts on a network range
Scans the top 1000 most common TCP ports
Detects:

Open ports
Running services
Software versions


Classifies each finding by risk level:

HIGH → MEDIUM → LOW


Automatically flags dangerous ports:

445 (SMB), 3389 (RDP), 22 (SSH), 21 (FTP), 23 (Telnet), 3306 (MySQL)


Generates a dark-themed HTML report
Skips unresponsive hosts automatically (timeout handling)

Tech Used

Python 3.x
Nmap 7.99
python-nmap library

Requirements

Python installed → python.org
Nmap installed → nmap.org/download.html
python-nmap library:

pip install python-nmap
How It Works
The scanner runs in 3 phases:
Phase 1 — Host Discovery
Sends ping probes across the entire network range to find which devices are alive
Phase 2 — Port Scanning
For each live host, scans the top 1000 ports and checks their state (open / closed / filtered)
Phase 3 — Report Generation
Compiles all results into a risk-rated HTML report saved in the reports/ folder
How To Run
python scanner.py 192.168.0.0/24
To find your network range run ipconfig (Windows) and check your IPv4 address.
If your IP is 192.168.1.45 then your range is 192.168.1.0/24
Note

This tool is for educational purposes and authorized testing only
Only scan networks you own or have written permission to test
Scanning without authorization is illegal

What I Learned

How ping sweeps discover live hosts on a network
Difference between open, closed, and filtered port states
How the TCP 3-way handshake relates to port scanning
What service fingerprinting is and how Nmap detects versions
Why ports like 445 and 3389 are high-risk findings in a pentest
Python concepts: functions, loops, exception handling, file I/O
How to control Nmap programmatically using python-nmap
CIDR notation and network ranges

Future Improvements

Add UDP port scanning
Add CVE lookup for detected service versions
Add JSON export option alongside HTML
Build a GUI version
Add OS detection

Project Portfolio
This is Project 2 of my 10-project cybersecurity portfolio.
#ProjectStatus1Password AnalyserDone2Network ScannerDone3Coming SoonIn Progress
Author
Hamza
