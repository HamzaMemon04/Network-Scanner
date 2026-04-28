import nmap
import sys

def discover_hosts(network_range):
    """
    Phase 1 - Host Discovery
    Finds all live devices on the network
    """

    print(f"\n[*] Starting host discovery on {network_range}")
    print("[*] This may take 10-30 seconds...\n")

    scanner = nmap.PortScanner()
    scanner.scan(hosts=network_range, arguments='-sn')
    live_hosts = scanner.all_hosts()

    print(f"[+] Host discovery complete.")
    print(f"[+] Found {len(live_hosts)} live host(s):\n")

    for host in live_hosts:
        hostname = scanner[host].hostname()
        if hostname:
            print(f"    {host}  ({hostname})")
        else:
            print(f"    {host}")

    return live_hosts


def scan_ports(host):
    """
    Phase 2 - Port Scanning
    Scans the most common 1000 ports on a single host
    """

    print(f"\n[*] Scanning ports on {host}...")

    scanner = nmap.PortScanner()

    try:
        scanner.scan(hosts=host, arguments='-sV --top-ports 1000 --host-timeout 30s')
    except Exception as e:
        print(f"    [!] Could not scan {host} - skipping. ({e})")
        return []

    open_ports = []

    if host in scanner.all_hosts():
        for proto in scanner[host].all_protocols():
            ports = scanner[host][proto].keys()
            for port in sorted(ports):
                state = scanner[host][proto][port]['state']
                if state == 'open':
                    service = scanner[host][proto][port]['name']
                    version = scanner[host][proto][port]['version']
                    product = scanner[host][proto][port]['product']

                    open_ports.append({
                        'port': port,
                        'proto': proto,
                        'service': service,
                        'product': product,
                        'version': version
                    })

                    print(f"    [OPEN] Port {port}/{proto}  ->  {service}  {product} {version}")

    if not open_ports:
        print(f"    No open ports found on {host}")

    return open_ports


def generate_report(all_results):
    """
    Phase 3 - Report Generation
    Generates a clean HTML report
    """
    import datetime

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"reports/scan_{timestamp}.html"

    total_open = sum(len(ports) for ports in all_results.values())

    host_rows = ""
    for host, ports in all_results.items():
        if not ports:
            host_rows += f"""
            <div class="host-card no-ports">
                <div class="host-header">
                    <span class="host-ip">{host}</span>
                    <span class="badge grey">No Open Ports</span>
                </div>
            </div>
            """
        else:
            port_rows = ""
            for p in ports:
                risk = "high" if p['port'] in [21,22,23,445,3389,3306] else "medium" if p['port'] in [80,8080,8443] else "low"
                port_rows += f"""
                <tr>
                    <td>{p['port']}/{p['proto']}</td>
                    <td>{p['service']}</td>
                    <td>{p['product']} {p['version']}</td>
                    <td><span class="risk {risk}">{risk.upper()}</span></td>
                </tr>
                """
            host_rows += f"""
            <div class="host-card">
                <div class="host-header">
                    <span class="host-ip">{host}</span>
                    <span class="badge green">{len(ports)} Open Port(s)</span>
                </div>
                <table>
                    <thead>
                        <tr>
                            <th>Port</th>
                            <th>Service</th>
                            <th>Version</th>
                            <th>Risk</th>
                        </tr>
                    </thead>
                    <tbody>
                        {port_rows}
                    </tbody>
                </table>
            </div>
            """

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Network Scan Report</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Courier New', monospace; background: #0a0a0a; color: #e0e0e0; padding: 40px; }}
        h1 {{ color: #00ff99; font-size: 28px; margin-bottom: 4px; }}
        .subtitle {{ color: #666; font-size: 13px; margin-bottom: 40px; }}
        .summary {{ display: flex; gap: 20px; margin-bottom: 40px; }}
        .stat-box {{ background: #111; border: 1px solid #222; padding: 20px 30px; border-radius: 8px; }}
        .stat-box .number {{ font-size: 32px; color: #00ff99; font-weight: bold; }}
        .stat-box .label {{ font-size: 12px; color: #666; margin-top: 4px; }}
        .host-card {{ background: #111; border: 1px solid #1e1e1e; border-radius: 8px; margin-bottom: 24px; overflow: hidden; }}
        .host-header {{ padding: 16px 20px; display: flex; align-items: center; gap: 16px; border-bottom: 1px solid #1e1e1e; }}
        .host-ip {{ font-size: 18px; color: #fff; font-weight: bold; }}
        .badge {{ padding: 4px 12px; border-radius: 20px; font-size: 12px; }}
        .badge.green {{ background: #003d1f; color: #00ff99; }}
        .badge.grey {{ background: #1a1a1a; color: #666; }}
        table {{ width: 100%; border-collapse: collapse; }}
        th {{ text-align: left; padding: 12px 20px; font-size: 11px; color: #666; text-transform: uppercase; letter-spacing: 1px; border-bottom: 1px solid #1e1e1e; }}
        td {{ padding: 12px 20px; font-size: 13px; border-bottom: 1px solid #151515; }}
        tr:last-child td {{ border-bottom: none; }}
        tr:hover td {{ background: #161616; }}
        .risk {{ padding: 2px 10px; border-radius: 4px; font-size: 11px; font-weight: bold; }}
        .risk.high {{ background: #3d0000; color: #ff4444; }}
        .risk.medium {{ background: #3d2600; color: #ff9900; }}
        .risk.low {{ background: #1a2a1a; color: #44aa44; }}
        .footer {{ margin-top: 40px; color: #333; font-size: 12px; }}
    </style>
</head>
<body>
    <h1>Network Scan Report</h1>
    <div class="subtitle">Generated: {datetime.datetime.now().strftime("%B %d, %Y at %H:%M:%S")}</div>

    <div class="summary">
        <div class="stat-box">
            <div class="number">{len(all_results)}</div>
            <div class="label">Live Hosts</div>
        </div>
        <div class="stat-box">
            <div class="number">{total_open}</div>
            <div class="label">Open Ports</div>
        </div>
    </div>

    {host_rows}

    <div class="footer">Generated by Network Scanner - Hamza's Cybersecurity Portfolio</div>
</body>
</html>"""

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"\n[+] Report saved -> {filename}")
    return filename


if __name__ == "__main__":

    if len(sys.argv) != 2:
        print("\nUsage:   python scanner.py <network_range>")
        print("Example: python scanner.py 192.168.0.0/24\n")
        sys.exit(1)

    network = sys.argv[1]

    # Phase 1 - discover live hosts
    live_hosts = discover_hosts(network)

    # Phase 2 - scan ports on each live host
    print("\n" + "="*50)
    print("PHASE 2 - PORT SCANNING")
    print("="*50)

    all_results = {}
    for host in live_hosts:
        open_ports = scan_ports(host)
        all_results[host] = open_ports

    print("\n[+] Port scanning complete.")

    # Phase 3 - generate report
    print("\n" + "="*50)
    print("PHASE 3 - GENERATING REPORT")
    print("="*50)

    generate_report(all_results)
    print("\n[+] Scan complete. Open the reports/ folder to view your report.")
