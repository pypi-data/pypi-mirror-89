import os
import requests
from helpers.log import get_logger

NASA_API_URL = "https://api.nasa.gov/"
NASA_API_KEY = os.environ.get('NASA_API_KEY', None)

logger = get_logger(__name__)

class NASAAPIKeyMissingError(Exception):
    pass

if NASA_API_KEY is None:
    raise NASAAPIKeyMissingError(
        "NASA classes require an API key. See "
        "https://api.nasa.gov/#signUp \n"
        "for how to retrieve an authentication token from "
        "NASA RESTful API\n"
        "Assign a value to your NASA_API_KEY as:\n"
        "NASA_API_KEY = 'YOUR_NASA_API_KEY'"
        )

try:
    session = requests.Session()
    session.params = {}
    session.params['api_key'] = NASA_API_KEY
    logger.info(f"Successfully spawned NASA")
except Exception as fatal_exception:
    logger.error(f"Fatal Exception occurred: {fatal_exception}")

from .APOD import APOD
from .DONKI import DONKI
from .Earth import EARTH 
from .EONET import EONET
from .EPIC import EPIC
from .Exoplanet import EXOPLANET
from .GeneLab import GENELAB
from .Images import IMAGES
from .Insight import INSIGHT
from .Mars import MARS
from .NEO import NEO
from .SSC import SSC
from .SSD_CNEOS import SSDCNEOS
from .Techport import TECHPORT
from .TechTransfer import TECHTRANSFER
from .TLE import TLE
from .WMTS import WMTS
