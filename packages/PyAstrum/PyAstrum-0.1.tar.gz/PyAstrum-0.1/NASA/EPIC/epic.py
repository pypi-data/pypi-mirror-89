from NASA import NASA_API_KEY, NASA_API_URL, session
from helpers.log import get_logger

logger = get_logger(__name__)

# BASE URLS
EPIC_URL = "EPIC/api"
EPIC_BIO_URL = "https://science.gsfc.nasa.gov/sed/bio"

# ENDPOINTS
NATURAL_ENDPOINT = "/natural"
NATURAL_DATE_ENDPOINT = "/natural/date/"
NATURAL_ALL_ENDPOINT = "/natural/all"
NATURAL_AVAILABLE_ENDPOINT = "/natural/available"
ENHANCED_ENDPOINT = "/enhanced"
ENHANCED_DATE_ENDPOINT = "/enhanced/date/"
ENHANCED_ALL_ENDPOINT = "/enhanced/all"
ENHANCED_AVAILABLE_ENDPOINT = "/enhanced/available"


class EPIC(object):
    """
    EPIC

    The EPIC API provides information on the daily imagery collected by
    DSCOVR's Earth Polychromatic Imaging Camera (EPIC) instrument. Uniquely
    positioned at the Earth-Sun Lagrange point, EPIC provides full disc imagery
    of the Earth and captures unique perspenhanced_available_urlectives of certain astronomical
    events such as lunar transits using a 2048x2048 pixel CCD (Charge Coupled
    Device) detector coupled to a 30-cm aperture Cassegrain telescope.

    Image metadata and key information are provided by the JSON API and can be
    requested by date and for the most recent available date. A listing of all
    available dates can also be retrieved via the API for more granular control.

    Development of the EPIC API began in 2015, and is supported by the web
    development team for the Laboratory for Atmospheres
    (http://atmospheres.gsfc.nasa.gov/) in the Earth Sciences Division of the
    Goddard Space Flight Center. More information regarding the API and
    retrieval of the imagery for download can be found on the EPIC website
    (http://epic.gsfc.nasa.gov/).

    NASA Official: Alexander Marshak ({EPIC_BIO_URL}/alexander.marshak-1)\n
    Image Curator: Carl Hostetter\n
    Webmasters:
    - Susannah Pearce ({EPIC_BIO_URL}/susannah.pearce)\n
    - Nathan Perrin ({EPIC_BIO_URL}/nathan.r.perrin)\n

    NOTE: NASA's API key from api.nasa.gov for expanded usage is required.
    """

    @staticmethod
    def get_natural_images():
        """
        Natural

        This endpoint retrieves metadata on the most recent date of natural
        color imagery.
        """
        session.params.clear()
        session.params['api_key'] = NASA_API_KEY
        natural_images_url = f"{NASA_API_URL}{EPIC_URL}{NATURAL_ENDPOINT}"
        try:
            response = session.get(natural_images_url)
            return response.json()
        except Exception as e:
            logger.error(f'Images unavailable because: {e}')

    @staticmethod
    def get_natural_date(date=None):
        """
        Natural Date

        This endpoint retrieves metadata for natural color imagery available
        for a given date.
        """
        session.params.clear()
        session.params['api_key'] = NASA_API_KEY
        try:
            if date is None:
                epic_natural_all_dates = EPIC.get_natural_all()
                epic_natural_first_date = epic_natural_all_dates[0]['date']
            else:
                epic_natural_first_date = date
            natural_date_url = f"{NASA_API_URL}{EPIC_URL}\
                                    {NATURAL_DATE_ENDPOINT}\
                                    {epic_natural_first_date}"
            response = session.get(natural_date_url)
            return response.json()
        except Exception as e:
            logger.error(f'Images unavailable because: {e}')

    @staticmethod
    def get_natural_all():
        """
        Natural All

        This endpoint retrieves a listing of all dates with available natural
        color imagery.
        """
        # TODO: Implement reverse: If True, start from the oldest date. Else
        # latest available date
        session.params.clear()
        session.params['api_key'] = NASA_API_KEY
        natural_all_url = f"{NASA_API_URL}{EPIC_URL}{NATURAL_ALL_ENDPOINT}"
        try:
            response = session.get(natural_all_url)
            return response.json()
        except Exception as e:
            logger.error(f'Dates unavailable because: {e}')

    @staticmethod
    def get_natural_available():
        """
        Natural Available

        This endpoint retrieves an alternate listing of all dates with
        available natural color imagery.
        """
        # TODO: Implement reverse: If True, start from the oldest date. Else
        # latest available date
        session.params.clear()
        session.params['api_key'] = NASA_API_KEY
        natural_available_url = f"{NASA_API_URL}{EPIC_URL}\
                                    {NATURAL_AVAILABLE_ENDPOINT}"
        try:
            response = session.get(natural_available_url)
            return response.json()
        except Exception as e:
            logger.error(f'Dates unavailable because: {e}')

    @staticmethod
    def get_enhanced_images():
        """
        Enhanced

        This endpoint retrieves metadata on the most recent date of enhanced
        color imagery.
        """
        session.params.clear()
        session.params['api_key'] = NASA_API_KEY
        enhanced_images_url = f"{NASA_API_URL}{EPIC_URL}{ENHANCED_ENDPOINT}"
        try:
            response = session.get(enhanced_images_url)
            return response.json()
        except Exception as e:
            logger.error(f'Images unavailable because: {e}')

    @staticmethod
    def get_enhanced_date(date=None):
        """
        Enhanced Date

        This endpoint retrieves metadata for enhanced color imagery for a given
        date.
        """
        session.params.clear()
        session.params['api_key'] = NASA_API_KEY
        try:
            if date is None:
                epic_enhanced_all_dates = EPIC.get_enhanced_all()
                epic_enhanced_first_date = epic_enhanced_all_dates[0]['date']
            else:
                epic_enhanced_first_date = date
            enhanced_date_url = f"{NASA_API_URL}{EPIC_URL}\
                                    {ENHANCED_DATE_ENDPOINT}\
                                    {epic_enhanced_first_date}"
            response = session.get(enhanced_date_url)
            return response.json()
        except Exception as e:
            logger.error(f'Image unavailable because: {e}')

    @staticmethod
    def get_enhanced_all():
        """
        Enhanced All

        This endpoint retrieves a listing of all dates with available enhanced
        color imagery.
        """
        session.params.clear()
        session.params['api_key'] = NASA_API_KEY
        enhanced_all_url = f"{NASA_API_URL}{EPIC_URL}{ENHANCED_ALL_ENDPOINT}"
        try:
            response = session.get(enhanced_all_url)
            return response.json()
        except Exception as e:
            logger.error(f'Dates unavailable because: {e}')

    @staticmethod
    def get_enhanced_available():
        """
        Enhanced Available

        This endpoint retrieves an alternate listing of all dates with
        available enhanced color imagery.
        """
        session.params.clear()
        session.params['api_key'] = NASA_API_KEY
        enhanced_available_url = f"{NASA_API_URL}{EPIC_URL}\
                                    {ENHANCED_AVAILABLE_ENDPOINT}"
        try:
            response = session.get(enhanced_available_url)
            return response.json()
        except Exception as e:
            logger.error(f'Dates unavailable because: {e}')

