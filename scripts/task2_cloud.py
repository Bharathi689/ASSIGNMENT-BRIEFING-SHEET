#!/usr/bin/python

"""
Task 2: Cloud Services Emulation with Render.com
Course: 7COM1076 Network Engineering
Student ID: 100
University of Hertfordshire
"""

from mininet.net import Mininet
from mininet.node import Controller, OVSKernelSwitch, NAT
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink

def topology():
    """Create network topology for cloud services emulation"""
    
    info("\n*** Starting Task 2: Cloud Services Emulation ***\n")
    info("Student ID: 100\n")
    info("Website: https://assignment-briefing-sheet.onrender.com\n\n")
    
    # Create network
    net = Mininet(
        controller=Controller,
        switch=OVSKernelSwitch,
        link=TCLink,
        autoSetMacs=True,
        autoStaticArp=True
    )

    info("*** Adding controller\n")
    c0 = net.addController('c0')

    info("*** Adding hosts\n")
    # H1 will access the internet
    h1 = net.addHost('h1', ip='10.0.0.1/24', defaultRoute='via 10.0.0.254')
    # H2 is a regular host
    h2 = net.addHost('h2', ip='10.0.0.2/24')

    info("*** Adding switches\n")
    s1 = net.addSwitch('s1')
    s2 = net.addSwitch('s2')
    s3 = net.addSwitch('s3')

    info("*** Creating links (Linear topology)\n")
    # Linear topology: h1 -- s1 -- s2 -- s3 -- h2
    net.addLink(h1, s1)
    net.addLink(s1, s2)
    net.addLink(s2, s3)
    net.addLink(s3, h2)

    info("*** Starting network\n")
    net.build()
    
    info("*** Starting controller and switches\n")
    c0.start()
    s1.start([c0])
    s2.start([c0])
    s3.start([c0])

    info("*** Adding NAT for internet connectivity\n")
    # NAT allows private network to access public internet
    nat = net.addNAT(name='nat0', connect=s1, ip='10.0.0.254', 
                     subnet='10.0.0.0/24', inetIntf=None)
    nat.configDefault()

    info("\n" + "="*70 + "\n")
    info("*** Network topology created successfully! ***\n")
    info("="*70 + "\n\n")
    
    info("Topology:\n")
    info("  [H1:10.0.0.1] -- [S1] -- [S2] -- [S3] -- [H2:10.0.0.2]\n")
    info("                    |                         \n")
    info("                  [NAT] -- Internet\n\n")
    
    info("="*70 + "\n")
    info("*** COMMANDS FOR TESTING AND SCREENSHOTS ***\n")
    info("="*70 + "\n\n")
    
    info("1. TEST INTERNET CONNECTIVITY:\n")
    info("   mininet> h1 ping -c 2 8.8.8.8\n")
    info("   📸 Take screenshot of successful ping\n\n")
    
    info("2. OPEN H1 TERMINAL (for xterm screenshots):\n")
    info("   mininet> xterm h1\n")
    info("   📸 Take screenshot of xterm window opening\n\n")
    
    info("3. IN H1 XTERM - INSTALL CURL:\n")
    info("   # apt-get update && apt-get install -y curl\n\n")
    
    info("4. IN H1 XTERM - ACCESS WEBSITE WITH CURL:\n")
    info("   # curl https://assignment-briefing-sheet.onrender.com\n")
    info("   📸 Take screenshot showing HTML output\n\n")
    
    info("5. IN H1 XTERM - INSTALL LYNX (text browser):\n")
    info("   # apt-get install -y lynx\n\n")
    
    info("6. IN H1 XTERM - VIEW WEBSITE IN LYNX:\n")
    info("   # lynx https://assignment-briefing-sheet.onrender.com\n")
    info("   📸 Take screenshot of webpage rendered in lynx\n")
    info("   (Press 'q' then 'y' to exit lynx)\n\n")
    
    info("7. ALTERNATIVE - CURL FROM MININET CLI:\n")
    info("   mininet> h1 curl https://assignment-briefing-sheet.onrender.com\n\n")
    
    info("8. TEST INTERNAL CONNECTIVITY:\n")
    info("   mininet> h1 ping -c 2 h2\n")
    info("   mininet> pingall\n\n")
    
    info("9. EXIT:\n")
    info("   mininet> exit\n\n")
    
    info("="*70 + "\n")
    info("*** Website URL: https://assignment-briefing-sheet.onrender.com ***\n")
    info("="*70 + "\n\n")

    # Start CLI
    CLI(net)

    info("*** Stopping network\n")
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    topology()
