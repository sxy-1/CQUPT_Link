import socket
import time

import psutil
import subprocess

import connect_wifi

# Set up the STARTUPINFO to hide the console window
startupinfo = subprocess.STARTUPINFO()
startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
startupinfo.wShowWindow = subprocess.SW_HIDE

def is_ethernet_connected():
    try:
        # 执行 ipconfig /all 命令
        result = subprocess.run(['ipconfig', '/all'], stdout=subprocess.PIPE, text=True, startupinfo=startupinfo)
        output = result.stdout

        # 检查输出中是否包含以太网连接并具有以 10. 开头的 IP 地址
        lines = output.splitlines()
        print(lines[5])
        ethernet_found = False
        for line in lines:
            if "Ethernet adapter" in line or "以太网适配器" in line:
                ethernet_found = True
            if ethernet_found and ("IPv4 Address" in line or "IPv4 地址" in line):
                if "10." in line.split(":")[1].strip():
                    return True
                ethernet_found = False
        return False
    except Exception as e:
        print(f"检查网络连接时出错: {e}")
        return False

def is_wlan_connected():
    try:
        # 执行 ipconfig /all 命令
        result = subprocess.run(['ipconfig', '/all'], stdout=subprocess.PIPE, text=True, startupinfo=startupinfo)
        output = result.stdout

        # 检查输出中是否包含以太网连接并具有以 10. 开头的 IP 地址
        lines = output.splitlines()
        ethernet_found = False
        for line in lines:
            if "Wireless LAN adapter" in line or "无线局域网适配器" in line:
                ethernet_found = True
            if ethernet_found and( "IPv4 Address" in line or "IPv4 地址" in line):
                if "10." in line.split(":")[1].strip():
                    return True
                ethernet_found = False
        return False
    except Exception as e:
        print(f"检查网络连接时出错: {e}")
        return False


def get_local_ip():
    try:
        # 检查有线连接并获取IP地址
        if is_ethernet_connected():
            interfaces = psutil.net_if_addrs().get("以太网")
            if interfaces:
                for address in interfaces:
                    if address.family == socket.AF_INET and address.address.startswith('10.'):
                        return "wired",address.address

        # 如果没有有线连接或者有线连接不是以 10. 开头，则返回无线IP地址
        if is_wlan_connected():
            interfaces = psutil.net_if_addrs().get("WLAN")
            if interfaces:
                for address in interfaces:
                    if address.family == socket.AF_INET and address.address.startswith('10.'):
                        return "wireless",address.address
        print("正在连接WiFi")
        connect_wifi.connect_to_wifi()
        time.sleep(10)
        # 下面一段与上面几乎相同 但是先连wifi
        if is_wlan_connected():

            time.sleep(15)
            interfaces = psutil.net_if_addrs().get("WLAN")
            if interfaces:
                for address in interfaces:
                    if address.family == socket.AF_INET and address.address.startswith('10.'):
                        return "wireless", address.address

        # 如果没有无线连接或者无线连接不是以 10. 开头，则返回 None
        return None,None

    except Exception as e:
        print(f"获取本地IP地址时出错: {e}")
        return None,None

if __name__ == "__main__":
    wire_kind,ip_address = get_local_ip()
    if ip_address:
        print("本地IP地址:", ip_address)
    else:
        print("无法获取本地IP地址")
