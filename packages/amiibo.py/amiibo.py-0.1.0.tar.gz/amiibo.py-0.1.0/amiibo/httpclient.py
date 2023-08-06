import sys
import requests
import aiohttp

from .errors import *

class HTTP(object):
    """Represent a HTTP client to send request."""

    __slots__ = ("user_agent",)

    def __init__(self) -> None:
        self.user_agent = "pyamiibo v{} Python/Python/ \
        {}.{} requests/{}".format("0.1.0", sys.version_info[0], sys.version_info[1], requests.__version__)

    def get(self, endpoint: str) -> dict:
        """Perform a GET request to the given URL
        
        Parameters
        ----------
        endpoint: :class:`str`
            The endpoint to request with.
        """

        url = "https://amiiboapi.com/{}".format(endpoint)
        req = requests.get(url, headers={"User-Agent": self.user_agent})
        if req.status_code == 200:
            return req.json()
        elif req.status_code == 404:
            raise NotFound("Request returned 404 code with message: {}".format((req.json())["error"]))
        elif req.status_code == 500:
            raise ServerDown("API is down right now.")

class AsyncHTTP(object):
    """Represent a Async HTTP Client"""


    __slots__ = ("session", "user_agent")

    def __init__(self) -> None:
        self.session = aiohttp.ClientSession()
        self.user_agent = self.user_agent = "pyamiibo v{} Python/Python/ \
        {}.{} aiohttp/{}".format("0.1.0", sys.version_info[0], sys.version_info[1], aiohttp.__version__)

    async def get(self, endpoint: str) -> dict:
        """Perform a GET Request to the given URL
        
        Parameters
        ----------
        endpoint: :class:`str`
            The endpoint to request with
        """
        url = "https://amiiboapi.com/{}".format(endpoint)
        req = await self.session.get(url)
        if req.status == 200:
            json = await req.json()
            return json
        elif req.status == 404:
            raise NotFound("Request returned 404 code with message: {}".format((req.json())["error"]))
        elif req.status_code == 500:
            raise ServerDown("API is down right now.")