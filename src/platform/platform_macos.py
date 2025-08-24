from __future__ import annotations

from typing import Optional, Tuple

from .platform_interface import IPlatform
from src.network_manager import NetworkMacOS


class PlatformMacOS(IPlatform):
    def name(self) -> str:
        return "macos"

    def get_network_manager(self):
        return NetworkMacOS()


