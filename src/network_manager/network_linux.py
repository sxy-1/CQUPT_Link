from src.network_manager.network_interface import INetwork


class NetworkLinux(INetwork):
    def connect_to_wifi(self) -> None:
        raise NotImplementedError("Linux WiFi connection is not implemented yet")

    def get_local_ip(self) -> str:
        raise NotImplementedError("Linux get local IP is not implemented yet")
