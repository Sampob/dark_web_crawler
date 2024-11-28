from stem import Signal
from stem.control import Controller

class TorMiddleware:
    def __init__(self, tor_proxy_port=8118, tor_control_port=9051):
        self.tor_proxy_port = tor_proxy_port
        self.tor_control_port = tor_control_port
        self.proxy = f"http://127.0.0.1:{tor_proxy_port}"

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            tor_proxy_port=crawler.settings.getint("TOR_PROXY_PORT", 8118),
            tor_control_port=crawler.settings.getint("TOR_CONTROL_PORT", 9051)
        )

    def renew_tor_ip(self):
        """Renew Tor circuit and get a new IP address"""
        try:
            with Controller.from_port(port=self.tor_control_port) as controller:
                controller.authenticate()
                controller.signal(Signal.NEWNYM)
        except Exception as e:
            print(f"Error renewing Tor IP: {e}")

    def process_request(self, request, spider):
        """Route request through Tor proxy"""
        request.meta["proxy"] = self.proxy
        return None

    def process_response(self, request, response, spider):
        """Optional: Check and handle Tor-related responses"""
        if response.status == 403 or response.status == 503:
            # Renew IP if blocked
            self.renew_tor_ip()
        return response