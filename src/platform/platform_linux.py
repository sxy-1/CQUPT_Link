from __future__ import annotations


from .platform_interface import IPlatform
from src.network_manager import NetworkLinux


class PlatformLinux(IPlatform):
    def name(self) -> str:
        return "linux"

    def get_network_manager(self):
        return NetworkLinux()



