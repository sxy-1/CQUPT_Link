import ctypes
import sys
import os
import platform
# import change_mac_csdn # 如果需要，可以取消注释


def is_admin():
    """
    确保脚本以管理员权限运行。
    如果当前没有管理员权限，则会提权并重新运行，然后退出当前进程。
    """
    system_name = platform.system()
    
    if system_name == "Windows":
        try:
            # 检查当前用户是否为管理员
            is_admin = ctypes.windll.shell32.IsUserAnAdmin()
        except AttributeError:
            # 在非 Windows 系统上，此函数不存在
            is_admin = False

        if not is_admin:
            # 如果不是管理员，则以管理员身份重新运行脚本
            # ShellExecuteW 会触发 UAC 弹窗
            ctypes.windll.shell32.ShellExecuteW(
                None, "runas", sys.executable, " ".join(sys.argv), None, 1
            )
            # 退出当前的非管理员进程
            sys.exit(0)
    
    elif system_name == "Darwin":  # macOS
        # 检查是否以root权限运行
        if os.geteuid() != 0:
            print("macOS系统检测到需要管理员权限")
            print("请使用 'sudo python3 CQUPT_Link.py' 运行程序")
            # 对于macOS，我们不自动提权，而是提示用户使用sudo
            # 因为GUI应用的sudo提权比较复杂
            return False
        return True
    
    elif system_name == "Linux":
        # 检查是否以root权限运行
        if os.geteuid() != 0:
            print("Linux系统检测到需要管理员权限")
            print("请使用 'sudo python3 CQUPT_Link.py' 运行程序")
            return False
        return True
    
    else:
        print(f"不支持的操作系统: {system_name}")
        return False
    
    return True


if __name__ == "__main__":
    # 在脚本开始时调用此函数

    if is_admin():
        # --- 以下是需要管理员权限才能执行的代码 ---
        print("脚本已成功以管理员身份运行。")
        # 在这里放置您需要管理员权限的其余代码
        # 例如: change_mac_csdn.change_mac(...)
        input("按 Enter 键退出...")  # 添加这行以便在控制台窗口中看到输出
    else:
        print("未获得管理员权限，程序退出。")
        sys.exit(1)
