import time

import subprocess
from Logger import log


# def query_wifi_networks():
#     command = "netsh wlan show networks mode=Bssid"
#     result = subprocess.run(command, capture_output=True, text=True, shell=True)
#     return result.stdout
#
# log.info(query_wifi_networks())

def connect_to_wifi():
    ssid_list = ["CQUPT-5G", "CQUPT", "CQUPT-2.4G"]
    for ssid in ssid_list:
        # 查看是否已连接
        time.sleep(2)
        result = subprocess.run(['netsh', 'wlan', 'show', 'interfaces'], capture_output=True, text=True)
        if "CQUPT" in result.stdout:
            log.info("已经连接")
            return
        log.info("未连接")
        subprocess.run(['netsh', 'wlan', 'connect', 'name=' + ssid, 'ssid=' + ssid, 'interface=WLAN'])
    # 循环连接校园网
    # Connect to WiFi using netsh command
    # subprocess.run(['netsh', 'interface', 'set', 'interface', 'Wi-Fi', 'enabled'], capture_output=True, text=True)


if __name__ == "__main__":
    # Create a virtual network adapter
    # Connect to WiFi
    ssid = "YourWiFiSSID"
    connect_to_wifi()
