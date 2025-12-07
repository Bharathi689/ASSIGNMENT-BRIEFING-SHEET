#!/usr/bin/python

"""
Task 2: Cloud Services Emulation
Course: 7COM1076 Network Engineering
University of Hertfordshire
"""

import sys
import os

# Add config directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'config'))

try:
    from student_config import STUDENT_ID, RENDER_URL, GITHUB_REPO
except ImportError:
    print("ERROR: Could not load student_config.py")
    print("Please ensure config/student_config.py exists")
    sys.exit(1)

from mininet.net import Mininet
from mininet.node import Controller, OVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink

def topology():
    """Create network topology for cloud service access"""
    
    # Validate configuration
    if RENDER_URL == "https://your-site.onrender.com":
        print("\n" + "="*70)
        print("WARNING: RENDER_URL not configured!")
        print("Please deploy your website to Render.com first,")
        print("then update RENDER_URL in config/student_config.py")
        print("\nContinue anyway for testing? (y/n): ", end='')
        choice = input().lower()
        if choice != 'y':
            return
        print("="*70 + "\n")
    
    info(f"\n*** Starting Task 2: Cloud Services Emulation ***\n")
    info(f"*** Student ID: {STUDENT_ID}\n")
    info(f"*** Target URL: {RENDER_URL}\n\n")
    
    net = Mininet(controller=Controller, link=TCLink, switch=OVSSwitch)

    info("*** Creating nodes\n")
    
    c0 = net.addController('c0')
    
    # Create 3 switches
    s1 = net.addSwitch('s1')
    s2 = net.addSwitch('s2')
    s3 = net.addSwitch('s3')
    
    # Create 2 hosts
    h1 = net.addHost('h1', ip='10.0.0.1/24')
    h2 = net.addHost('h2', ip='10.0.0.2/24')

    info("*** Creating links\n")
    net.addLink(h1, s1)
    net.addLink(h2, s3)
    net.addLink(s1, s2)
    net.addLink(s2, s3)

    info("*** Starting network\n")
    net.build()
    c0.start()
    s1.start([c0])
    s2.start([c0])
    s3.start([c0])

    info("*** Configuring NAT for internet access\n")
    h1.cmd('ip route add default via 10.0.0.254')
    h1.cmd('echo "nameserver 8.8.8.8" > /etc/resolv.conf')
    
    h2.cmd('ip route add default via 10.0.0.254')
    h2.cmd('echo "nameserver 8.8.8.8" > /etc/resolv.conf')
    
    net.addNAT(ip='10.0.0.254').configDefault()
    
    info("\n" + "="*70 + "\n")
    info("*** Network Configuration Complete!\n")
    info("="*70 + "\n\n")
    
    info("*** TASK 2 STEP-BY-STEP INSTRUCTIONS:\n\n")
    info("STEP 1: Open xterm for h1\n")
    info("   Command in Mininet CLI: xterm h1 &\n\n")
    
    info("STEP 2: In h1 xterm, test internet connectivity:\n")
    info("   ping -c 4 8.8.8.8\n")
    info("   (Take screenshot)\n\n")
    
    info("STEP 3: Test DNS resolution:\n")
    render_domain = RENDER_URL.replace('https://', '').replace('http://', '')
    info(f"   nslookup {render_domain}\n")
    info("   (Take screenshot)\n\n")
    
    info("STEP 4: Access your website using curl:\n")
    info(f"   curl {RENDER_URL}\n")
    info("   (Take screenshot showing HTML)\n\n")
    
    info("STEP 5: Download and view webpage:\n")
    info(f"   wget {RENDER_URL} -O index.html\n")
    info("   cat index.html\n")
    info("   (Take screenshot)\n\n")
    
    info("OPTIONAL: Use text browser (if lynx installed):\n")
    info(f"   lynx {RENDER_URL}\n\n")
    
    info("="*70 + "\n")
    info("*** Configuration Summary:\n")
    info(f"   Student ID: {STUDENT_ID}\n")
    info(f"   Website URL: {RENDER_URL}\n")
    info(f"   GitHub Repo: {GITHUB_REPO}\n")
    info(f"   H1 IP: 10.0.0.1/24\n")
    info(f"   H2 IP: 10.0.0.2/24\n")
    info(f"   Gateway: 10.0.0.254\n")
    info(f"   DNS: 8.8.8.8\n")
    info("="*70 + "\n\n")
    
    CLI(net)

    info("*** Stopping network\n")
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    topology()
