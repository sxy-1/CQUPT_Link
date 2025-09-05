from src.network_manager.network_interface import INetwork


class NetworkMacOS(INetwork):
    def connect_to_wifi(self) -> None:
        raise NotImplementedError("macOS WiFi connection is not implemented yet")

    def get_local_ip(self) -> str:
        raise NotImplementedError("macOS get local IP is not implemented yet")
