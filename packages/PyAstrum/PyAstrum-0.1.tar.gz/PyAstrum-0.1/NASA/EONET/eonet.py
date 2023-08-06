from NASA import NASA_API_KEY, NASA_API_URL, session
from helpers.log import get_logger

logger = get_logger(__name__)

EONET_URL = "https://eonet.sci.gsfc.nasa.gov"


class EONET(object):
    """
    EONET

    The Earth Observatory Natural Event Tracker (EONET) is a prototype web
    service with the goal of:
    - Providing a curated source of continuously updated natural event metadata
    - Providing a service that links those natural events to thematically-related
        web service-enabled image sources (e.g., via WMS, WMTS, etc.).

    Development of EONET began in 2015 and has been supported by NASA’s Earth
    Observatory and Earth Science Data and Information System (ESDIS) Project.

    NASA's Earth Observatory: http://earthobservatory.nasa.gov/
    ESDIS: https://earthdata.nasa.gov/about/esdis-project
    """
    # TODO: Implement NASA's EONET external API on:
    # https://eonet.sci.gsfc.nasa.gov/docs/v2.1
    pass