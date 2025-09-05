# 转载修改自 Csdn : https://blog.csdn.net/zhu6201976

import ctypes
import platform
import random
import re
import subprocess
import sys
from Logger import log
import config

# 只在Windows上导入Windows特定的模块
if platform.system() == "Windows":
    import winreg
    import chardet

class SetMac(object):
    """
    跨平台修改 MAC地址
    """

    def __init__(self, kind="wireless"):
        # regex to MAC address like 00-00-00-00-00-00 or 00:00:00:00:00:00 or
        # 000000000000
        self.MAC_ADDRESS_RE = re.compile(r"""
            ([0-9A-F]{1,2})[:-]?
            ([0-9A-F]{1,2})[:-]?
            ([0-9A-F]{1,2})[:-]?
            ([0-9A-F]{1,2})[:-]?
            ([0-9A-F]{1,2})[:-]?
            ([0-9A-F]{1,2})
            """, re.I | re.VERBOSE)  # re.I: case-insensitive matching. re.VERBOSE: just look nicer.

        self.kind = kind
        self.system = platform.system()
        
        if self.system == "Windows":
            self.WIN_REGISTRY_PATH = "SYSTEM\CurrentControlSet\Control\Class\{4D36E972-E325-11CE-BFC1-08002BE10318}"
            # Set up the STARTUPINFO to hide the console window
            self.startupinfo = subprocess.STARTUPINFO()
            self.startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            self.startupinfo.wShowWindow = subprocess.SW_HIDE

    def is_admin(self):
        """
        检查是否有管理员权限
        :return:
        """
        if self.system == "Windows":
            if ctypes.windll.shell32.IsUserAnAdmin() == 0:
                log.info('Sorry! You should run this with administrative privileges if you want to change your MAC address.')
                sys.exit()
            else:
                log.info('admin')
        elif self.system == "Darwin":  # macOS
            import os
            if os.geteuid() != 0:
                log.info('macOS需要管理员权限来修改MAC地址，请使用sudo运行')
                return False
            else:
                log.info('macOS admin权限确认')
        else:
            log.warning(f'不支持的操作系统: {self.system}')

    def get_macinfos(self):
        """
        查看所有mac信息
        :return:
        """
        log.info('=' * 50)
        try:
            if self.system == "Windows":
                mac_info = subprocess.check_output('GETMAC /v /FO list', stderr=subprocess.STDOUT, startupinfo=self.startupinfo)
                # 使用chardet检测编码
                result = chardet.detect(mac_info)
                encoding = result['encoding']
                config.set_config_value("encoding",encoding)
                mac_info = mac_info.decode(config.get_config_value("encoding"))
                log.info('Your MAC address:\n '+'\n'.join(mac_info.split('\n')[:11]))
            elif self.system == "Darwin":  # macOS
                # 在macOS上获取网络接口信息
                result = subprocess.run(['ifconfig'], capture_output=True, text=True)
                log.info('macOS网络接口信息:\n' + result.stdout[:1000])  # 限制输出长度
        except subprocess.CalledProcessError as e:
            log.info(f"获取MAC信息出错: {e}")

    def get_target_device(self):
        """
        返回目标网络适配器
        :return:
        """
        if self.system == "Windows":
            mac_info = subprocess.check_output('GETMAC /v /FO list', stderr=subprocess.STDOUT, startupinfo=self.startupinfo)
            # 使用chardet检测编码
            result = chardet.detect(mac_info)
            encoding = result['encoding']
            config.set_config_value("encoding", encoding)
            mac_info = mac_info.decode(config.get_config_value("encoding"))

            if self.kind == "wireless":
                search = re.search(r'(WLAN)\s+(网络适配器:|Network Adapter:)(.+)\s+(物理地址:|Physical Address:)', mac_info)
            else:
                search = re.search(r'(本地连接|以太网)\s+(网络适配器:|Network Adapter:)(.+)\s+(物理地址:|Physical Address:)', mac_info)
            target_name, target_device = (search.group(1), search.group(3).strip()) if search else ('', '')
            if not all([target_name, target_device]):
                log.info('Cannot find the target device')
                sys.exit()

            log.info("target_name "+target_name)
            log.info("target_device "+target_device)
            return target_device
        elif self.system == "Darwin":  # macOS
            # 在macOS上返回标准的网络接口名
            if self.kind == "wireless":
                return "en0"  # 通常WiFi接口
            else:
                return "en1"  # 通常有线接口

    def generate_random_mac(self):
        # 第一个字节必须是2、6、A或E (本地管理位设置)
        first_byte = random.choice([0x02, 0x06, 0x0A, 0x0E])

        # 生成剩余的5个字节
        remaining_bytes = [random.randint(0x00, 0xff) for _ in range(5)]

        # 组合成MAC地址
        mac_address = [first_byte] + remaining_bytes
        mac_address_str = "".join(["%02X" % byte for byte in mac_address])

        return mac_address_str

    def set_mac_address(self, target_device, new_mac):
        """
        设置新mac地址
        :param target_device: 网络适配器
        :param new_mac: 新mac地址
        :return:
        """
        if not self.MAC_ADDRESS_RE.match(new_mac):
            log.info('Please input a correct MAC address')
            return
        log.info("当前setmac: "+new_mac)
        
        if self.system == "Windows":
            self._set_mac_windows(target_device, new_mac)
        elif self.system == "Darwin":  # macOS
            self._set_mac_macos(target_device, new_mac)
        else:
            log.warning(f'不支持的操作系统: {self.system}')

    def _set_mac_windows(self, target_device, new_mac):
        """Windows下设置MAC地址"""
        # Locate adapter's registry and update network address (mac)
        reg_hdl = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)
        key = winreg.OpenKey(reg_hdl, self.WIN_REGISTRY_PATH)
        info = winreg.QueryInfoKey(key)

        # Find adapter key based on sub keys
        adapter_key = None
        adapter_path = None
        target_index = -1

        for index in range(info[0]):
            subkey = winreg.EnumKey(key, index)
            path = self.WIN_REGISTRY_PATH + "\\" + subkey

            if subkey == 'Properties':
                break

            # Check for adapter match for appropriate interface
            new_key = winreg.OpenKey(reg_hdl, path)
            try:
                adapterDesc = winreg.QueryValueEx(new_key, "DriverDesc")
                if adapterDesc[0] == target_device:
                    adapter_path = path
                    target_index = index
                    break
                else:
                    winreg.CloseKey(new_key)
            except (WindowsError) as err:
                if err.errno == 2:  # register value not found, ok to ignore
                    pass
                else:
                    raise err

        if adapter_path is None:
            log.info('Device not found.')
            winreg.CloseKey(key)
            winreg.CloseKey(reg_hdl)
            return
        
        # Registry path found update mac addr
        adapter_key = winreg.OpenKey(reg_hdl, adapter_path, 0, winreg.KEY_WRITE)
        winreg.SetValueEx(adapter_key, "NetworkAddress", 0, winreg.REG_SZ, new_mac)
        winreg.CloseKey(adapter_key)
        winreg.CloseKey(key)
        winreg.CloseKey(reg_hdl)

        # Adapter must be restarted in order for change to take affect
        self.restart_adapter(target_index, target_device)

    def _set_mac_macos(self, target_device, new_mac):
        """macOS下设置MAC地址"""
        try:
            # 格式化MAC地址为 xx:xx:xx:xx:xx:xx
            formatted_mac = ':'.join([new_mac[i:i+2] for i in range(0, len(new_mac), 2)])
            log.info(f"尝试在macOS上设置{target_device}的MAC地址为: {formatted_mac}")
            
            # 在macOS上，通常需要先关闭接口，设置MAC，然后重新启用
            # 注意：这需要管理员权限
            
            # 方法1: 使用ifconfig (需要root权限)
            try:
                # 关闭接口
                subprocess.run(['sudo', 'ifconfig', target_device, 'down'], check=True)
                # 设置MAC地址
                subprocess.run(['sudo', 'ifconfig', target_device, 'ether', formatted_mac], check=True)
                # 重新启用接口
                subprocess.run(['sudo', 'ifconfig', target_device, 'up'], check=True)
                log.info(f"成功设置MAC地址: {formatted_mac}")
            except subprocess.CalledProcessError as e:
                log.warning(f"ifconfig方法失败: {e}")
                # 方法2: 尝试使用airport工具 (仅适用于WiFi)
                if target_device == "en0" and self.kind == "wireless":
                    try:
                        # 断开WiFi连接
                        subprocess.run(['sudo', '/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport', '-z'], check=True)
                        # 设置MAC地址 (这在现代macOS上可能不工作)
                        log.warning("macOS系统限制：无法直接修改WiFi MAC地址")
                        log.info("建议：在macOS上，MAC地址随机化由系统管理")
                    except subprocess.CalledProcessError as e:
                        log.warning(f"WiFi MAC修改失败: {e}")
                        
        except Exception as e:
            log.warning(f"macOS MAC地址修改失败: {e}")
            log.info("注意：现代macOS系统出于隐私考虑，限制了MAC地址的修改")

    def restart_adapter(self, target_index, target_device):
        """
        重启网络适配器
        """
        if self.system == "Windows":
            if platform.release() == 'XP':
                # Windows XP处理方式
                cmd = "devcon hwids =net"
                try:
                    result = subprocess.check_output(cmd, stderr=subprocess.STDOUT, startupinfo=self.startupinfo)
                except FileNotFoundError:
                    raise
                query = '(' + target_device + '\r\n\s*.*:\r\n\s*)PCI\\\\(([A-Z]|[0-9]|_|&)*)'
                query = query.encode('ascii')
                match = re.search(query, result)
                cmd = 'devcon restart "PCI\\' + str(match.group(2).decode('ascii')) + '"'
                subprocess.check_output(cmd, stderr=subprocess.STDOUT, startupinfo=self.startupinfo)
            else:
                # 现代Windows处理方式
                cmd = "wmic path win32_networkadapter where index=" + str(target_index) + " call disable"
                subprocess.check_output(cmd, startupinfo=self.startupinfo)
                cmd = "wmic path win32_networkadapter where index=" + str(target_index) + " call enable"
                subprocess.check_output(cmd, startupinfo=self.startupinfo)
        elif self.system == "Darwin":  # macOS
            # macOS上的接口重启已在_set_mac_macos中处理
            log.info("macOS网络接口重启完成")

    def run(self, new_mac=None):
        if not self.is_admin():
            return False
            
        self.get_macinfos()
        target_device = self.get_target_device()
        if new_mac is None:
            self.set_mac_address(target_device, self.generate_random_mac())
        else:
            self.set_mac_address(target_device, new_mac)
        self.get_macinfos()
        return True


if __name__ == '__main__':
    set_mac = SetMac("wireless")
    set_mac.run()