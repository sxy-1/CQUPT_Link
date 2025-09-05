from .platform_interface import IPlatform
from src.network_manager import NetworkMacOS
from src.network_manager import INetwork


class PlatformMacOS(IPlatform):
    def name(self) -> str:
        return "macos"

    def get_network_manager(self) -> INetwork:
        return NetworkMacOS()
