#!/usr/bin/python

"""
Task 1: WiFi Network Emulation with Mobility
Course: 7COM1076 Network Engineering
University of Hertfordshire
"""

import sys
import os

# Add config directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'config'))

try:
    from student_config import *
except ImportError:
    print("ERROR: Could not load student_config.py")
    print("Please ensure config/student_config.py exists and is properly configured")
    sys.exit(1)

from mininet.node import Controller
from mininet.log import setLogLevel, info
from mn_wifi.net import Mininet_wifi
from mn_wifi.node import OVSKernelAP
from mn_wifi.cli import CLI
from mn_wifi.link import wmediumd
from mn_wifi.wmediumdConnector import interference
import time

def topology():
    """Create WiFi network topology with mobility"""
    
    # Validate configuration
    if STUDENT_ID == "YOUR_STUDENT_ID_HERE":
        print("\n" + "="*60)
        print("ERROR: Please configure your student ID!")
        print("Edit: config/student_config.py")
        print("Change STUDENT_ID to your actual student ID")
        print("="*60 + "\n")
        return
    
    info(f"\n*** Starting Task 1 with Student ID: {STUDENT_ID} ***\n\n")
    
    net = Mininet_wifi(
        controller=Controller,
        link=wmediumd,
        wmediumd_mode=interference,
        noise_th=-91
    )

    info("*** Creating nodes\n")
    
    # Create Access Points
    ap1 = net.addAccessPoint('AP1', ssid=SSID, mode='g', 
                            channel=AP_CONFIGS['AP1']['channel'],
                            passwd=PASSWORD, encrypt='wpa2',
                            failMode='standalone', datapath='user',
                            position=AP_CONFIGS['AP1']['position'],
                            range=AP_CONFIGS['AP1']['range'])
    
    ap2 = net.addAccessPoint('AP2', ssid=SSID, mode='g',
                            channel=AP_CONFIGS['AP2']['channel'],
                            passwd=PASSWORD, encrypt='wpa2',
                            failMode='standalone', datapath='user',
                            position=AP_CONFIGS['AP2']['position'],
                            range=AP_CONFIGS['AP2']['range'])
    
    ap3 = net.addAccessPoint('AP3', ssid=SSID, mode='g',
                            channel=AP_CONFIGS['AP3']['channel'],
                            passwd=PASSWORD, encrypt='wpa2',
                            failMode='standalone', datapath='user',
                            position=AP_CONFIGS['AP3']['position'],
                            range=AP_CONFIGS['AP3']['range'])

    # Create Stations
    sta1 = net.addStation('UE1', ip=STATION_CONFIGS['UE1']['ip'],
                         position=STATION_CONFIGS['UE1']['start_pos'],
                         passwd=PASSWORD, encrypt='wpa2')
    
    sta2 = net.addStation('UE2', ip=STATION_CONFIGS['UE2']['ip'],
                         position=STATION_CONFIGS['UE2']['start_pos'],
                         passwd=PASSWORD, encrypt='wpa2')

    c0 = net.addController('c0')

    net.setPropagationModel(model="logDistance", exp=4)

    info("*** Configuring WiFi nodes\n")
    net.configureWifiNodes()

    info("*** Creating links (Linear topology)\n")
    net.addLink(ap1, ap2)
    net.addLink(ap2, ap3)

    info("*** Starting network\n")
    net.build()
    c0.start()
    ap1.start([c0])
    ap2.start([c0])
    ap3.start([c0])

    info("*** Configuring mobility\n")
    net.startMobility(time=0, model='RandomDirection',
                     max_x=100, max_y=100, 
                     min_v=STATION_CONFIGS['UE1']['min_speed'],
                     max_v=STATION_CONFIGS['UE1']['max_speed'])
    
    # UE1 mobility
    ue1_cfg = STATION_CONFIGS['UE1']
    net.mobility(sta1, 'start', time=ue1_cfg['start_time'], 
                position=ue1_cfg['start_pos'])
    net.mobility(sta1, 'stop', time=ue1_cfg['end_time'], 
                position=ue1_cfg['end_pos'])
    
    # UE2 mobility
    ue2_cfg = STATION_CONFIGS['UE2']
    net.mobility(sta2, 'start', time=ue2_cfg['start_time'],
                position=ue2_cfg['start_pos'])
    net.mobility(sta2, 'stop', time=ue2_cfg['end_time'],
                position=ue2_cfg['end_pos'])
    
    net.stopMobility(time=61)

    info("\n*** Waiting for initial setup (5 seconds)...\n")
    time.sleep(5)
    
    info("\n*** Configuration Summary:\n")
    info("="*60 + "\n")
    info(f"Student ID: {STUDENT_ID}\n")
    info(f"SSID: {SSID}\n")
    info(f"Encryption: WPA2\n")
    info(f"Noise Threshold: -91dBm\n")
    info(f"Topology: Linear (AP1 -- AP2 -- AP3)\n")
    info("="*60 + "\n")
    
    info("\n*** IMPORTANT COMMANDS FOR SCREENSHOTS:\n")
    info("="*60 + "\n")
    info("1. Show GUI (before mobility):\n")
    info("   py net.plotGraph(max_x=100, max_y=100)\n\n")
    info("2. Wait 61 seconds for mobility to complete\n\n")
    info("3. Show GUI (after mobility):\n")
    info("   py net.plotGraph(max_x=100, max_y=100)\n\n")
    info("4. Check UE1 connection:\n")
    info("   sta UE1 iw dev UE1-wlan0 link\n\n")
    info("5. Check UE2 connection:\n")
    info("   sta UE2 iw dev UE2-wlan0 link\n\n")
    info("6. Ping test:\n")
    info("   UE1 ping -c 4 UE2\n\n")
    info("7. Exit:\n")
    info("   exit\n")
    info("="*60 + "\n\n")
    
    CLI(net)

    info("*** Stopping network\n")
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    topology()
