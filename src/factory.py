import platform
from src.platform import IPlatform
from src.platform import PlatformWindows
from src.platform import PlatformLinux
from src.platform import PlatformMacOS


class Factory:
    @staticmethod
    def create_platform() -> IPlatform:
        # 获取当前平台，并返回对应的实现
        platform_name = platform.system()

        if platform_name == "Windows":
            return PlatformWindows()
        elif platform_name == "Linux":
            return PlatformLinux()
        elif platform_name == "Darwin":  # macOS
            return PlatformMacOS()
        else:
            raise ValueError(f"Unsupported platform: {platform_name}")
