from src.platform.platform_interface import IPlatform
from src.network_manager import NetworkWindows


class PlatformWindows(IPlatform):
    def name(self) -> str:
        return "windows"

    def get_network_manager(self) -> NetworkWindows:
        return NetworkWindows()
