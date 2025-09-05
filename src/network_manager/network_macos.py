from src.network_manager.network_interface import INetwork
import subprocess
import socket
import time
import psutil
from Logger import log


class NetworkMacOS(INetwork):
    def __init__(self):
        # macOS不需要特殊的启动信息配置
        pass

    def connect_to_wifi(self) -> None:
        """连接到CQUPT校园网WiFi"""
        ssid_list = ["CQUPT-5G", "CQUPT", "CQUPT-2.4G"]
        
        for ssid in ssid_list:
            try:
                # 检查是否已连接
                time.sleep(2)
                result = subprocess.run(
                    ["/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport", "-I"],
                    capture_output=True, 
                    text=True
                )
                
                if ssid in result.stdout:
                    log.info(f"已经连接到 {ssid}")
                    return
                
                log.info(f"尝试连接到 {ssid}")
                # 使用networksetup连接WiFi
                subprocess.run([
                    "networksetup", 
                    "-setairportnetwork", 
                    "en0",  # 通常WiFi接口是en0
                    ssid
                ], capture_output=True)
                
                # 检查连接是否成功
                time.sleep(5)
                result = subprocess.run(
                    ["/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport", "-I"],
                    capture_output=True, 
                    text=True
                )
                
                if ssid in result.stdout:
                    log.info(f"成功连接到 {ssid}")
                    return
                    
            except Exception as e:
                log.warning(f"连接WiFi {ssid} 时出错: {e}")
                continue
        
        log.warning("未能连接到任何可用的Wi-Fi")

    def _is_ethernet_connected(self) -> bool:
        """检查以太网是否连接并获得10.x.x.x的IP"""
        try:
            # 获取所有网络接口
            interfaces = psutil.net_if_addrs()
            
            # 检查有线网络接口（通常是en1, en2等）
            for interface_name, addresses in interfaces.items():
                if interface_name.startswith('en') and interface_name != 'en0':  # en0通常是WiFi
                    for address in addresses:
                        if (address.family == socket.AF_INET and 
                            address.address.startswith('10.')):
                            log.info(f"检测到有线连接: {interface_name} - {address.address}")
                            return True
            return False
        except Exception as e:
            log.warning(f"检查有线连接时出错: {e}")
            return False

    def _is_wifi_connected(self) -> bool:
        """检查WiFi是否连接并获得10.x.x.x的IP"""
        try:
            # 获取WiFi接口信息（通常是en0）
            interfaces = psutil.net_if_addrs().get("en0")
            if interfaces:
                for address in interfaces:
                    if (address.family == socket.AF_INET and 
                        address.address.startswith('10.')):
                        log.info(f"检测到WiFi连接: en0 - {address.address}")
                        return True
            return False
        except Exception as e:
            log.warning(f"检查WiFi连接时出错: {e}")
            return False

    def get_local_ip(self) -> tuple:
        """获取本地IP地址，返回(连接类型, IP地址)"""
        try:
            # 检查有线连接
            if self._is_ethernet_connected():
                interfaces = psutil.net_if_addrs()
                for interface_name, addresses in interfaces.items():
                    if interface_name.startswith('en') and interface_name != 'en0':
                        for address in addresses:
                            if (address.family == socket.AF_INET and 
                                address.address.startswith('10.')):
                                return "wired", address.address

            # 检查WiFi连接
            if self._is_wifi_connected():
                interfaces = psutil.net_if_addrs().get("en0")
                if interfaces:
                    for address in interfaces:
                        if (address.family == socket.AF_INET and 
                            address.address.startswith('10.')):
                            return "wireless", address.address

            # 如果没有连接，尝试连接WiFi
            log.info("正在连接WiFi")
            self.connect_to_wifi()
            time.sleep(10)
            
            # 再次检查WiFi连接
            if self._is_wifi_connected():
                time.sleep(5)  # 等待IP分配
                interfaces = psutil.net_if_addrs().get("en0")
                if interfaces:
                    for address in interfaces:
                        if (address.family == socket.AF_INET and 
                            address.address.startswith('10.')):
                            return "wireless", address.address

            # 如果都没有连接成功
            return None, None

        except Exception as e:
            log.warning(f"获取本地IP地址时出错: {e}")
            return None, None
