from NASA import NASA_API_KEY, NASA_API_URL, session
from helpers.log import get_logger

logger = get_logger(__name__)

# BASE URLS
IMAGES_URL = "https://images-api.nasa.gov/"

# ENDPOINTS
SEARCH_ENDPOINT = "search?q="
ASSET_ENDPOINT = "asset/"
METADATA_ENDPOINT = "metadata/"
CAPTIONS_ENDPOINT = "captions/"

class IMAGES(object):
    """
    NASA Image and Video Library
    Use this API to access the NASA Image and Video Library site at
    images.nasa.gov.

    The images.nasa.gov API is organized around REST, has
    predictable/resource­-oriented URLs and uses HTTP response codes to
    indicate API errors. This API uses built-­in HTTP features such as HTTP
    authentication and HTTP verbs, which are understood by many off-­the-­shelf
    HTTP clients. Please note that JSON is returned by all API responses,
    including errors. Each of the endpoints described below also contains
    example snippets which use the curl command­-line tool, Unix pipelines,
    and the python command­-line tool to output API responses in an easy­ to
    ­read format.

    Available Endpoints
    The images API contains 4 endpoints GET https://images-api.nasa.gov

    GET /search?q={q}	    Performing a search
    GET /asset/{nasa_id}	Retrieving a media asset’s manifest
    GET /metadata/{nasa_id}	Retrieving a media asset’s metadata location
    GET /captions/{nasa_id}	Retrieving a video asset’s captions location
    
    For complete usage information and detailed examples, please visit the
    NASA Image and Video Library API documentation.
    """


    @staticmethod
    def search(query=None):
        """
        Perform a search

        GET /search?q={query}

        :param query: query string
        :return: response dict
        """
        session.params.clear()
        search_url = f"{IMAGES_URL}{SEARCH_ENDPOINT}{query}"
        try:
            response = session.get(search_url)
            return response.json()
        except Exception as e:
            logger.error(f'Search results unavailable because: {e}')


    @staticmethod
    def get_asset_for(nasa_id=None):
        """
        Retrieves a media asset’s manifest

        GET /asset/{nasa_id}

        :param nasa_id: NASA media asset ID
        :return: manifest dict
        """
        session.params.clear()
        asset_url = f"{IMAGES_URL}{ASSET_ENDPOINT}{nasa_id}"
        try:
            response = session.get(asset_url)
            return response.json()
        except Exception as e:
            logger.error(f'Asset unavailable because: {e}')


    @staticmethod
    def get_metadata_for(nasa_id=None):
        """
        Retrieves a media asset’s metadata location

        GET /metadata/{nasa_id}

        :param nasa_id: NASA media asset ID
        :return: metadata dictGET /metadata/{nasa_id}
        """
        session.params.clear()
        metadata_url = f"{IMAGES_URL}{METADATA_ENDPOINT}{nasa_id}"
        try:
            response = session.get(metadata_url)
            return response.json()
        except Exception as e:
            logger.error(f'Metadata unavailable because: {e}')


    @staticmethod
    def get_captions_for(nasa_id=None):
        """
        Retrieves a video asset’s captions location

        GET /captions/{nasa_id}

        :param nasa_id: NASA media asset ID
        :return: captions dict
        """
        session.params.clear()
        captions_url = f"{IMAGES_URL}{CAPTIONS_ENDPOINT}{nasa_id}"
        try:
            response = session.get(captions_url)
            return response.json()
        except Exception as e:
            logger.error(f'Captions unavailable because: {e}')
