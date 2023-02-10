import codecs
import mmh3
import requests
import socket
from urllib.parse import urlparse

socket.setdefaulttimeout(10)
from walkoff_app_sdk.app_base import AppBase

class FaviconHasher(AppBase):
    __version__ = "1.0.0"
    app_name = "favicon_hasher"
    scheme = "https://"
    favicon = "/favicon.ico"

    def __init__(self, redis, logger, console_logger=None):
        super().__init__(redis, logger, console_logger)

    def validateUri(uri):
        try:
            result = urlparse(uri)
            return all([result.scheme, result.netloc])
        except:
            return False

    def create_hash(self, domain):

        uri = "".join([self.scheme, domain, self.favicon])
        if validateuri(uri):
            try:
                resp = requests.get(uri)
                favicon = codecs.encode(resp.content,"base64")
                hash = mmh3.hash(favicon)
                return hash
            except requests.exceptions.HTTPError as err:
                return {
                    "success": False,
                    "reason": "An error happened when fetching favicon",
                    "details": f"{err}"
                }
        else:
            return {
                    "success": False,
                    "reason": "Malformatted URI",
                    "details": f"URI: {uri}"
                }


if __name__ == "__main__":
    FaviconHasher.run()