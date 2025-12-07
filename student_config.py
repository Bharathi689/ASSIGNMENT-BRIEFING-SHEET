"""
Student Configuration File
IMPORTANT: UPDATE ALL VALUES WITH YOUR ACTUAL DETAILS!
"""

# ============================================
# TASK 1 CONFIGURATION
# ============================================
STUDENT_ID = "YOUR_STUDENT_ID_HERE"  # ⚠️ CHANGE THIS TO YOUR ACTUAL STUDENT ID!
SSID = STUDENT_ID
PASSWORD = STUDENT_ID

AP_CONFIGS = {
    'AP1': {
        'position': '30,50,0',
        'channel': '1',
        'range': 50
    },
    'AP2': {
        'position': '60,50,0',
        'channel': '6',
        'range': 50
    },
    'AP3': {
        'position': '90,50,0',
        'channel': '11',
        'range': 50
    }
}

STATION_CONFIGS = {
    'UE1': {
        'ip': '192.168.1.1/24',
        'start_pos': '10,30,0',
        'end_pos': '60,50,0',
        'start_time': 10,
        'end_time': 20,
        'min_speed': 1,
        'max_speed': 5
    },
    'UE2': {
        'ip': '192.168.1.2/24',
        'start_pos': '10,30,0',
        'end_pos': '90,50,0',
        'start_time': 30,
        'end_time': 60,
        'min_speed': 5,
        'max_speed': 10
    }
}

# ============================================
# TASK 2 CONFIGURATION
# ============================================
RENDER_URL = "https://your-site.onrender.com"  # ⚠️ UPDATE after deploying to Render.com
GITHUB_REPO = "https://github.com/yourusername/your-repo"  # ⚠️ UPDATE with your repo URL

# ============================================
# TASK 3 CONFIGURATION
# ============================================
# ⚠️ CHECK YOUR ASSIGNMENT SHEET FOR THESE VALUES!
ASSIGNED_HOST = "h1"  # Example: "h3", "h7", etc. - CHECK YOUR ASSIGNMENT!
ASSIGNED_SERVER = "server1"  # Example: "server1", "server2", or "server3" - CHECK YOUR ASSIGNMENT!
ASSIGNED_PORT = 5566  # Example: Your assigned port number - CHECK YOUR ASSIGNMENT!

SERVER_IPS = {
    'server1': '20.0.0.2',
    'server2': '40.0.0.2',
    'server3': '60.0.0.2'
}

HOST_IP_BASE = "172.16.0"
ONOS_IP = "127.0.0.1"
ONOS_PORT = 6653
ONOS_GUI_PORT = 8181

# ============================================
# TESTING CONFIGURATION
# ============================================
PING_COUNT = 4
UDP_TEST_DURATION = 600  # seconds (10 minutes)
UDP_BANDWIDTH = "100M"