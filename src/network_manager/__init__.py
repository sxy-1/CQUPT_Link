from .network_interface import INetwork
from .network_windows import NetworkWindows
from .network_linux import NetworkLinux
from .network_macos import NetworkMacOS
__all__ = [
    "INetwork",
    "NetworkWindows",
    "NetworkLinux",
    "NetworkMacOS",
]
