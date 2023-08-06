from NASA import NASA_API_KEY, NASA_API_URL, session
from datetime import datetime as dt
from helpers.log import get_logger

logger = get_logger(__name__)

# BASE URL
EARTH_URL = "/planetary/earth/"

# ENDPOINTS
ASSETS_ENDPOINT = "assets"
IMAGERY_ENDPOINT = "imagery"

# MISCELLANEOUS
NASA_HEADQUARTER_LAT = 38.8829823
NASA_HEADQUARTER_LON = -77.0166355
TODAY = dt.utcnow().isoformat()


class EARTH(object):
    """
    EARTH

    Landsat imagery is provided to the public as a joint project between
    NASA and USGS. Earth Data is powered by EOSDIS.

    NASA's Earth Observing System Data and Information System (EOSDIS) is a key
    core capability in the Earth Science Data Systems (ESDS) Program.
    It provides end-to-end capabilities for managing NASA Earth science data
    from various sources—satellites, aircraft, field measurements, and various
    other programs. For the EOS satellite missions, EOSDIS provides
    capabilities for command and control, scheduling, data capture and initial
    (level 0) processing. These capabilities, constituting the EOSDIS Mission
    Operations, are managed by NASA's Earth Science Mission Operations (ESMO)
    Project. NASA network capabilities transport the data to the science
    operations facilities.

    EOSDIS: https://earthdata.nasa.gov/eosdis\n
    ESDS: https://earthdata.nasa.gov/earth-science-data-systems-program\n
    ESMO: http://espd.gsfc.nasa.gov/esmo/index.html\n
    """

    @staticmethod
    def get_images(latitude=NASA_HEADQUARTER_LAT,
                    longitude=NASA_HEADQUARTER_LON,
                    date=TODAY,
                    dim=0.025):
        """
        Imagery

        This endpoint retrieves the Landsat 8 image for the supplied location
        and date. The response will include the date and URL to the image that
        is closest to the supplied date. The requested resource may not be
        available for the exact date in the request.

        :param: lat: Latitude
        :param: lon: Longitude
        :param: date: default is current UTC date. Beginning of 30 day date
        range that will be used to look for closest image to that date
        :param: dim: width and height of image in degrees
        """
        session.params.clear()
        session.params['lat'] = latitude
        session.params['lon'] = longitude
        session.params['date'] = date
        session.params['dim'] = dim
        session.params['api_key'] = NASA_API_KEY
        imagery_url = f"{NASA_API_URL}{EARTH_URL}{IMAGERY_ENDPOINT}"
        try:
            response = session.get(imagery_url)
            return response.json()
        except Exception as e:
            logger.error(f'Images unavailable because: {e}')

    @staticmethod
    def get_assets(latitude=NASA_HEADQUARTER_LAT,
                    longitude=NASA_HEADQUARTER_LON,
                    date=TODAY,
                    dim=0.025):
        """
        Assets

        This endpoint retrieves the date-times and asset names for closest
        available imagery for a supplied location and date. The satellite
        passes over each point on earth roughly once every sixteen days.

        :param: lat: Latitude
        :param: lon: Longitude
        :param: date: default is current UTC date. Beginning of 30 day date
        range that will be used to look for closest image to that date
        :param: dim: width and height of image in degrees
        """
        session.params.clear()
        session.params['lat'] = latitude
        session.params['lon'] = longitude
        session.params['date'] = date
        session.params['dim'] = dim
        session.params['api_key'] = NASA_API_KEY
        assets_url = f"{NASA_API_URL}{EARTH_URL}{ASSETS_ENDPOINT}"
        try:
            response = session.get(assets_url)
            return response.json()
        except Exception as e:
            logger.error(f'Assets unavailable because: {e}')
