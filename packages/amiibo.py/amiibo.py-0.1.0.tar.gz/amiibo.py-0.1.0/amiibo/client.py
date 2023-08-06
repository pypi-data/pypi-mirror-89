from .errors import *
from .httpclient import HTTP, AsyncHTTP

class Client(object):
    """Represent a Amiibo Client to perform requests with API"""

    __slots__ = ("_http",)

    def __init__(self) -> None:
        self._http = HTTP()

    def last_updated(self) -> dict:
        """Get the timestamp where the amiibo API was last updated."""

        endpoint = "api/lastupdated/"
        req = self._http.get(endpoint)
        return req

    def get_amiibos(self) -> dict:
        """Return a list of amiibos available in the API"""

        endpoint = "api/amiibo/"
        req = self._http.get(endpoint)
        return req

    def get_amiibo(self, **kwargs) -> dict:
        """Return the information about a single amiibo with given arguments
        
        Available arguments:
            head, tail, name, type

        If head and tail is given other params would be ignored and request as id=head+tail

        For more information see: https://amiiboapi.com/docs/#amiibo
        """

        head = kwargs.get("head")
        tail = kwargs.get("tail")
        name = kwargs.get("name")
        amiiboo_type = kwargs.get("type")
        if head and tail:
            amiibo_id = head + tail
            endpoint = "api/amiibo/?id={}".format(amiibo_id)
            req = self._http.get(endpoint)
            return req
        elif name != None and amiiboo_type != None:
            endpoint = "api/amiibo/?name={}&type={}".format(name, amiiboo_type)
            req = self._http.get(endpoint)
            return req
        else:
            raise MissingArgumet("Either head, tail or name, type should be given")

    def get_type(self, amiibo_type: str) -> dict:
        """Get all the amiibo based on it's type as a list.
        
        Parameters
        ----------

        amiibo_type: :class:`str`
            The amiibo type. Eg. `0x02`, `yarn`
        """

        endpoint = "api/amiibo/?type={}".format(amiibo_type)
        req = self._http.get(endpoint)
        return req

    def get_gameseries(self, gameseries: str) -> dict:
        """Get all the amiibo based on it's game series as a list.
        
        Parameters
        ----------
        gameseries: :class:`str`
            The gameseries to request.
        """

        endpoint = "api/amiibo/?gameseries={}".format(gameseries)
        req = self._http.get(endpoint)
        return req

    def get_series(self, amiiboSeries: str) -> dict:
        """Get all the amiibo based on it's series as a list.
        
        Parameters
        ----------
        amiiboSeries: :class:`str`
            The series to get the data
        """

        endpoint = "api/amiibo/?amiiboSeries={}".format(amiiboSeries)
        req = self._http.get(endpoint)
        return req

    def get_character(self, character: str) -> dict:
        """Get all the amiibo based on it's character as a list
        
        Parameters
        ----------
        character: :class:`str`
            the character to get the data
        """

        endpoint = "api/amiibo/?character={}".format(character)
        req = self._http.get(endpoint)
        return req

    def get_types(self) -> dict:
        """Get all the amiibo's type available in the API as a list"""

        endpoint = "/api/type"
        req = self._http.get(endpoint)
        return req

    def get_type_by_id(self, type_id: str) -> dict:
        """Get type by it's id
        
        Parameters
        ----------
        type_id: :class:`str`
            The type id to get the data
        """

        endpoint = "api/type?key={}".format(type_id)
        req = self._http.get(endpoint)
        return req
    
    def get_type_by_name(self, name: str) -> dict:
        """Get type by it's name
        
        Parameters
        ----------
        name: :class:`str`
            The name to get the data
        """

        endpoint = "api/type?name={}".format(name)
        req = self._http.get(endpoint)
        return req

    def get_gameserieses(self) -> dict:
        """Retrieve game series information, not all data return a list"""

        endpoint = "api/gameseries/"
        req = self._http.get(endpoint)
        return req

    def get_gameseries_by_key(self, key: str) -> dict:
        """It just return the game series that the key belongs to, since 1 key only belongs to 1 game series
        
        Parameters
        ----------
        key: :class:`str`
            The key that we need to get the data
        """

        endpoint = "api/gameseries?key={}".format(key)
        req = self._http.get(endpoint)
        return req

    def get_gameseries_keys(self, name: str) -> dict:
        """It return a list of keys available for the game series
        
        Parameters
        ----------
        name: :class:`str`
            The gameseries name which we need to fetch the data.
        """

        endpoint = "api/gameseries?name={}".format(name)
        req = self._http.get(endpoint)
        return req

    def get_serieses(self) -> dict:
        """Get all the amiibo's series available in the API as a list."""

        endpoint = "api/amiiboseries/"
        req = self._http.get(endpoint)
        return req

    def get_series_by_key(self, key: str) -> dict:
        """Get the amiibo series by it's key
        
        Parameters
        ----------
        key: :class:`str`
            The key that we need to get the data
        """

        endpoint = "api/amiiboseries?key={}".format(key)
        req = self._http.get(endpoint)
        return req

    def get_series_by_name(self, name: str) -> dict:
        """Get the amiibo series by it's name
        
        Parameters
        ----------
        name: :class:`str`
            The name that we need to get the data
        """

        endpoint = "api/amiiboseries?name={}".format(name)
        req = self._http.get(endpoint)
        return req

    def get_characters(self) -> dict:
        """Get all the character available in the API as a list."""

        endpoint = "api/character"
        req = self._http.get(endpoint)
        return req
    
    def get_character_by_key(self, key: str) -> dict:
        """Get the character by it's key
        
        Parameters
        ----------

        key: :class:`str`
            The key that we use to get the data
        """

        endpoint = "api/character?key={}".format(key)
        req = self._http.get(endpoint)
        return req

    def get_character_by_name(self, name: str) -> dict:
        """Get the character by it's key
        
        Parameters
        ----------

        name: :class:`str`
            The name that we use to get the data
        """

        endpoint = "api/character?name={}".format(name)
        req = self._http.get(endpoint)
        return req

class AsyncClient(object):
    """Represent a Amiibo Client to perform requests with API"""

    __slots__ = ("_http",)

    async def __init__(self) -> None:
        self._http = AsyncHTTP()

    async def last_updated(self) -> dict:
        """Get the timestamp where the amiibo API was last updated."""

        endpoint = "api/lastupdated/"
        req = await self._http.get(endpoint)
        return req

    async def get_amiibos(self) -> dict:
        """Return a list of amiibos available in the API"""

        endpoint = "api/amiibo/"
        req = await self._http.get(endpoint)
        return req

    async def get_amiibo(self, **kwargs) -> dict:
        """Return the information about a single amiibo with given arguments
        
        Available arguments:
            head, tail, name, type

        If head and tail is given other params would be ignored and request as id=head+tail

        For more information see: https://amiiboapi.com/docs/#amiibo
        """

        head = kwargs.get("head")
        tail = kwargs.get("tail")
        name = kwargs.get("name")
        amiiboo_type = kwargs.get("type")
        if head and tail:
            amiibo_id = head + tail
            endpoint = "api/amiibo/?id={}".format(amiibo_id)
            req = await self._http.get(endpoint)
            return req
        elif name != None and amiiboo_type != None:
            endpoint = "api/amiibo/?name={}&type={}".format(name, amiiboo_type)
            req = await self._http.get(endpoint)
            return req
        else:
            raise MissingArgumet("Either head, tail or name, type should be given")

    async def get_type(self, amiibo_type: str) -> dict:
        """Get all the amiibo based on it's type as a list.
        
        Parameters
        ----------

        amiibo_type: :class:`str`
            The amiibo type. Eg. `0x02`, `yarn`
        """

        endpoint = "api/amiibo/?type={}".format(amiibo_type)
        req = await self._http.get(endpoint)
        return req

    async def get_gameseries(self, gameseries: str) -> dict:
        """Get all the amiibo based on it's game series as a list.
        
        Parameters
        ----------
        gameseries: :class:`str`
            The gameseries to request.
        """

        endpoint = "api/amiibo/?gameseries={}".format(gameseries)
        req = await self._http.get(endpoint)
        return req

    async def get_series(self, amiiboSeries: str) -> dict:
        """Get all the amiibo based on it's series as a list.
        
        Parameters
        ----------
        amiiboSeries: :class:`str`
            The series to get the data
        """

        endpoint = "api/amiibo/?amiiboSeries={}".format(amiiboSeries)
        req = await self._http.get(endpoint)
        return req

    async def get_character(self, character: str) -> dict:
        """Get all the amiibo based on it's character as a list
        
        Parameters
        ----------
        character: :class:`str`
            the character to get the data
        """

        endpoint = "api/amiibo/?character={}".format(character)
        req = await self._http.get(endpoint)
        return req

    async def get_types(self) -> dict:
        """Get all the amiibo's type available in the API as a list"""

        endpoint = "/api/type"
        req = await self._http.get(endpoint)
        return req

    async def get_type_by_id(self, type_id: str) -> dict:
        """Get type by it's id
        
        Parameters
        ----------
        type_id: :class:`str`
            The type id to get the data
        """

        endpoint = "api/type?key={}".format(type_id)
        req = await self._http.get(endpoint)
        return req
    
    async def get_type_by_name(self, name: str) -> dict:
        """Get type by it's name
        
        Parameters
        ----------
        name: :class:`str`
            The name to get the data
        """

        endpoint = "api/type?name={}".format(name)
        req = await self._http.get(endpoint)
        return req

    async def get_gameserieses(self) -> dict:
        """Retrieve game series information, not all data return a list"""

        endpoint = "api/gameseries/"
        req = await self._http.get(endpoint)
        return req

    async def get_gameseries_by_key(self, key: str) -> dict:
        """It just return the game series that the key belongs to, since 1 key only belongs to 1 game series
        
        Parameters
        ----------
        key: :class:`str`
            The key that we need to get the data
        """

        endpoint = "api/gameseries?key={}".format(key)
        req = await self._http.get(endpoint)
        return req

    async def get_gameseries_keys(self, name: str) -> dict:
        """It return a list of keys available for the game series
        
        Parameters
        ----------
        name: :class:`str`
            The gameseries name which we need to fetch the data.
        """

        endpoint = "api/gameseries?name={}".format(name)
        req = await self._http.get(endpoint)
        return req

    async def get_serieses(self) -> dict:
        """Get all the amiibo's series available in the API as a list."""

        endpoint = "api/amiiboseries/"
        req = await self._http.get(endpoint)
        return req

    async def get_series_by_key(self, key: str) -> dict:
        """Get the amiibo series by it's key
        
        Parameters
        ----------
        key: :class:`str`
            The key that we need to get the data
        """

        endpoint = "api/amiiboseries?key={}".format(key)
        req = await self._http.get(endpoint)
        return req

    async def get_series_by_name(self, name: str) -> dict:
        """Get the amiibo series by it's name
        
        Parameters
        ----------
        name: :class:`str`
            The name that we need to get the data
        """

        endpoint = "api/amiiboseries?name={}".format(name)
        req = await self._http.get(endpoint)
        return req

    async def get_characters(self) -> dict:
        """Get all the character available in the API as a list."""

        endpoint = "api/character"
        req = await self._http.get(endpoint)
        return req
    
    async def get_character_by_key(self, key: str) -> dict:
        """Get the character by it's key
        
        Parameters
        ----------

        key: :class:`str`
            The key that we use to get the data
        """

        endpoint = "api/character?key={}".format(key)
        req = await self._http.get(endpoint)
        return req

    async def get_character_by_name(self, name: str) -> dict:
        """Get the character by it's key
        
        Parameters
        ----------

        name: :class:`str`
            The name that we use to get the data
        """

        endpoint = "api/character?name={}".format(name)
        req = await self._http.get(endpoint)
        return req