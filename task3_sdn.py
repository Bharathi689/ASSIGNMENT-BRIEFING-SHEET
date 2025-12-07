#!/usr/bin/python

"""
Task 3: Software Defined Networking with ONOS
Course: 7COM1076 Network Engineering
University of Hertfordshire
"""

import sys
import os

# Add config directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'config'))

try:
    from student_config import (STUDENT_ID, ASSIGNED_HOST, ASSIGNED_SERVER, 
                                ASSIGNED_PORT, SERVER_IPS, HOST_IP_BASE,
                                ONOS_IP, ONOS_PORT, UDP_TEST_DURATION, 
                                UDP_BANDWIDTH)
except ImportError:
    print("ERROR: Could not load student_config.py")
    print("Please ensure config/student_config.py exists")
    sys.exit(1)

from mininet.net import Mininet
from mininet.node import RemoteController, OVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink
import time

def topology():
    """Create SDN topology with ONOS controller"""
    
    # Validate configuration
    if ASSIGNED_HOST == "h1" and ASSIGNED_SERVER == "server1" and ASSIGNED_PORT == 5566:
        print("\n" + "="*70)
        print("WARNING: Using default assignment values!")
        print("Please check your assignment sheet and update:")
        print("  - ASSIGNED_HOST in config/student_config.py")
        print("  - ASSIGNED_SERVER in config/student_config.py")
        print("  - ASSIGNED_PORT in config/student_config.py")
        print("\nContinue with defaults? (y/n): ", end='')
        choice = input().lower()
        if choice != 'y':
            return
        print("="*70 + "\n")
    
    info(f"\n*** Starting Task 3: SDN with ONOS Controller ***\n")
    info(f"*** Student ID: {STUDENT_ID}\n")
    info(f"*** Assigned Host: {ASSIGNED_HOST}\n")
    info(f"*** Assigned Server: {ASSIGNED_SERVER}\n")
    info(f"*** Assigned Port: {ASSIGNED_PORT}\n\n")
    
    net = Mininet(controller=RemoteController, link=TCLink, switch=OVSSwitch)

    info("*** Creating ONOS controller connection\n")
    c0 = net.addController('c0', controller=RemoteController,
                          ip=ONOS_IP, port=ONOS_PORT)
    
    info("*** Creating switches (linear topology)\n")
    switches = []
    for i in range(1, 14):
        s = net.addSwitch(f's{i}', protocols='OpenFlow13')
        switches.append(s)
    
    info("*** Creating 10 hosts with Class B addresses (172.16.0.0/16)\n")
    hosts = []
    for i in range(1, 11):
        h = net.addHost(f'h{i}', 
                       ip=f'{HOST_IP_BASE}.{i}/16',
                       mac=f'00:00:00:00:00:{i:02x}')
        hosts.append(h)
        info(f"   Created h{i}: {HOST_IP_BASE}.{i}/16\n")
    
    info("*** Creating 3 servers\n")
    server1 = net.addHost('server1', ip='20.0.0.2/8',
                         mac='00:00:00:00:01:01')
    server2 = net.addHost('server2', ip='40.0.0.2/8',
                         mac='00:00:00:00:01:02')
    server3 = net.addHost('server3', ip='60.0.0.2/8',
                         mac='00:00:00:00:01:03')
    
    servers = [server1, server2, server3]
    info("   Created server1: 20.0.0.2/8\n")
    info("   Created server2: 40.0.0.2/8\n")
    info("   Created server3: 60.0.0.2/8\n")

    info("*** Creating links (linear topology)\n")
    # Connect hosts to switches
    for i, host in enumerate(hosts):
        net.addLink(host, switches[i])
    
    # Connect servers to switches
    for i, server in enumerate(servers):
        net.addLink(server, switches[10 + i])
    
    # Connect switches linearly
    for i in range(len(switches) - 1):
        net.addLink(switches[i], switches[i + 1])
    
    info(f"   Total links: {len(hosts) + len(servers) + len(switches) - 1}\n")

    info("*** Starting network\n")
    net.build()
    
    info("*** Starting controller and switches\n")
    c0.start()
    for switch in switches:
        switch.start([c0])

    info("\n*** Waiting for ONOS to discover topology (15 seconds)...\n")
    info("*** IMPORTANT: Ensure ONOS is running!\n")
    info(f"*** ONOS GUI: http://localhost:8181/onos/ui (onos/rocks)\n\n")
    
    time.sleep(15)

    # Print configuration summary
    info("\n" + "="*70 + "\n")
    info("*** NETWORK CONFIGURATION COMPLETE ***\n")
    info("="*70 + "\n\n")
    
    info("HOSTS (Class B - 172.16.0.0/16):\n")
    for i in range(1, 11):
        info(f"  h{i:2d}: {HOST_IP_BASE}.{i}/16  MAC: 00:00:00:00:00:{i:02x}\n")
    
    info("\nSERVERS:\n")
    info("  server1: 20.0.0.2/8  MAC: 00:00:00:00:01:01\n")
    info("  server2: 40.0.0.2/8  MAC: 00:00:00:00:01:02\n")
    info("  server3: 60.0.0.2/8  MAC: 00:00:00:00:01:03\n")
    
    info("\nYOUR ASSIGNMENT:\n")
    info(f"  Host: {ASSIGNED_HOST}\n")
    info(f"  Server: {ASSIGNED_SERVER} ({SERVER_IPS[ASSIGNED_SERVER]})\n")
    info(f"  Port: {ASSIGNED_PORT}\n")
    info("="*70 + "\n\n")

    # Test connectivity
    info("*** Testing Connectivity\n")
    info(f"*** Testing {ASSIGNED_HOST} to all servers...\n\n")
    
    assigned_host_obj = net.get(ASSIGNED_HOST)
    assigned_server_obj = net.get(ASSIGNED_SERVER)
    
    for server in servers:
        info(f"Ping {ASSIGNED_HOST} -> {server.name} ({server.IP()})...\n")
        result = assigned_host_obj.cmd(f'ping -c 4 {server.IP()}')
        info(result + "\n")
    
    info("\n" + "="*70 + "\n")
    info("*** UDP PERFORMANCE TEST INSTRUCTIONS ***\n")
    info("="*70 + "\n\n")
    
    info("YOUR TEST CONFIGURATION:\n")
    info(f"  Duration: {UDP_TEST_DURATION} seconds (10 minutes)\n")
    info(f"  Bandwidth: {UDP_BANDWIDTH}\n")
    info(f"  Host: {ASSIGNED_HOST}\n")
    info(f"  Server: {ASSIGNED_SERVER} ({SERVER_IPS[ASSIGNED_SERVER]})\n")
    info(f"  Port: {ASSIGNED_PORT}\n\n")
    
    info("STEP-BY-STEP PROCEDURE:\n\n")
    info("1. Open xterm windows:\n")
    info(f"   xterm {ASSIGNED_HOST} {ASSIGNED_SERVER} &\n\n")
    
    info(f"2. In {ASSIGNED_SERVER} xterm, start iperf server:\n")
    info(f"   iperf -s -u -p {ASSIGNED_PORT}\n\n")
    
    info(f"3. In {ASSIGNED_HOST} xterm, start iperf client:\n")
    info(f"   iperf -c {SERVER_IPS[ASSIGNED_SERVER]} -u -p {ASSIGNED_PORT} -b {UDP_BANDWIDTH} -t {UDP_TEST_DURATION}\n\n")
    
    info("4. Wait for test to complete (10 minutes)\n\n")
    info("5. Take screenshots of BOTH terminals\n\n")
    
    info("="*70 + "\n")
    info("*** USEFUL CLI COMMANDS ***\n")
    info("="*70 + "\n")
    info("  pingall                    # Test all connectivity\n")
    info(f"  {ASSIGNED_HOST} ping -c 10 {SERVER_IPS[ASSIGNED_SERVER]}  # Quick ping\n")
    info(f"  xterm {ASSIGNED_HOST} {ASSIGNED_SERVER}        # Open terminals\n")
    info("  net                        # Show topology\n")
    info("  links                      # Show links\n")
    info("  dump                       # Show node info\n")
    info("  exit                       # Exit\n")
    info("="*70 + "\n\n")
    
    CLI(net)

    info("*** Stopping network\n")
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    topology()