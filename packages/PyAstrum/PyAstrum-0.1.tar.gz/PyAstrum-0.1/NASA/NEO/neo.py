from NASA import NASA_API_KEY, NASA_API_URL, session
from datetime import datetime as dt, timedelta
from helpers.log import get_logger

logger = get_logger(__name__)

# BASE URL
NEO_URL = 'neo/rest/v1/'

# ENDPOINTS
BROWSE_ENDPOINT = 'neo/browse'
FEED_ENDPOINT = 'feed'
LOOKUP_ENDPOINT = 'neo/'

# MISCELLANEOUS
DATE_ISO_FORMAT = "YYYY-MM-DD"
DEFAULT_PAGE = 1
DEFAULT_SIZE = 20
DEFAULT_ASTEROID_ID = 3542519
TODAY = dt.utcnow().isoformat()
A_WEEK_AGO = TODAY - timedelta(days=7)


class NEO(object):
    """
    NEO

    NASA Jet Propulsion Laboratory\n
    California Institute of Technology\n
    Solar System Dynamics\n
    
    NeoWs (Near Earth Object Web Service) is a RESTful web service for near
    earth Asteroid information. With NeoWs a user can: search for Asteroids
    based on their closest approach date to Earth, lookup a specific asteroid
    with its NASA JPL small body id (SPK-ID), as well as browse the overall
    data-set.

    'Asteroids - NeoWs' (Near Earth Object Web Service) API is maintained
    API is maintained by SpaceRocks Team (https://github.com/SpaceRocks/):
    David Greenfield, Arezu Sarvestani, Jason English and Peter Baunach.

    Data-set is from NASA JPL Asteroid team:\n
    http://neo.jpl.nasa.gov/

    JPL Small-Body Database Search Engine:\n
    http://ssd.jpl.nasa.gov/sbdb_query.cgi
    """

    __slots__ = ['asteroid_id', 'start_date', 'end_date']


    def __init__(self, asteroid_id=None, start_date=A_WEEK_AGO, end_date=TODAY):
        self.asteroid_id = asteroid_id
        self.start_date = start_date
        self.end_date = end_date

    ##### ASTEROID_ID #####
    @property
    def asteroid_id(self):
        """
        The docstring for the asteroid_id property
        Asteroid SPK-ID correlates to the NASA JPL small body.
        Conforms: to SPK-ID | Example: 3542519
        """
        return self._asteroid_id

    @asteroid_id.setter
    def asteroid_id(self, value):
        """
        The docstring for the asteroid_id property setter
        """
        if isinstance(value, int) or value is None:
            self._asteroid_id = value
            logger.info(f"Setting value of path to {value}")
        else:
            logger.error(f"Error: {value} is not a valid asteroid ID integer")

    @asteroid_id.deleter
    def asteroid_id(self):
        """
        The docstring for the asteroid_id property deleter
        """
        logger.debug('Deleting asteroid_id attribute')
        del self._asteroid_id

    ##### START_DATE #####
    @property
    def start_date(self):
        """
        The docstring for the start_date property
        Starting date for asteroid search.
        Conforms: to DATE_FORMAT | Example: 2015-09-07
        """
        return self._start_date

    @start_date.setter
    def start_date(self, value):
        """
        The docstring for the start_date property setter
        """
        if value is None:
            self._start_date = value
        else:
            try:
                _ = dt.strptime(value, DATE_ISO_FORMAT)
                self._start_date = value
        
            except ValueError as value_error:
                logger.error(f"{value_error}: {value} is not a valid start_date string")

    @start_date.deleter
    def start_date(self):
        """
        The docstring for the start_date property deleter
        """
        logger.debug('Deleting start_date attribute')
        del self._start_date

    ##### END_DATE #####
    @property
    def end_date(self):
        """
        The docstring for the end_date property
        Ending date for asteroid search. By default, 7 days after
        start_date.
        Conforms: to DATE_FORMAT | Example: 2015-09-08
        """
        return self._end_date

    @end_date.setter
    def end_date(self, value):
        """
        The docstring for the end_date property setter
        """
        if value is None:
            self._end_date = value
        else:
            try:
                _ = dt.strptime(value, DATE_ISO_FORMAT)
                self._end_date = value

            except ValueError as value_error:
                logger.error(f"{value_error}: {value} is not a valid end_date string")

    @end_date.deleter
    def end_date(self):
        """
        The docstring for the end_date property deleter
        """
        logger.debug('Deleting end_date attribute')
        del self._end_date

    ##### INFO #####
    def info(self):
        """
        The docstring for the info method
        Information of the latest Asteroid search parameters
        """
        return {
                'asteroid_id': self.asteroid_id,
                'start_date': self.start_date,
                'end_date': self.end_date
            }

    ##### GET_FEED #####
    def get_feed(self, start_date=A_WEEK_AGO, end_date=TODAY):
        """
        The docstring for the get_feed method
        Retrieve a list of Asteroids based on their closest approach date to
        Earth.
        """
        session.params.clear()
        session.params['start_date'] = start_date
        session.params['end_date'] = end_date
        session.params['api_key'] = NASA_API_KEY
        feed_url = f"{NASA_API_URL}{NEO_URL}{FEED_ENDPOINT}"
        try:
            response = session.get(feed_url)
            return response.json()
        except Exception as e:
            logger.error(f'Feed unavailable because: {e}')

    ##### GET_ASTEROID #####
    def get_asteroid(self, asteroid_id=None):
        """
        The docstring for the get_asteroid method
        Lookup a specific Asteroid based on its NASA JPL small body (SPK-ID) ID
        """
        if asteroid_id is None:
            asteroid_id = self.asteroid_id
        session.params.clear()
        session.params['asteroid_id'] = asteroid_id
        session.params['api_key'] = NASA_API_KEY
        look_up_url = f"{NASA_API_URL}{NEO_URL}{LOOKUP_ENDPOINT}"
        try:
            response = session.get(look_up_url)
            return response.json()
        except Exception as e:
            logger.error(f'Asteroid unavailable because: {e}')

    ##### BROWSE #####
    def browse(self):
        """
        The docstring for the browse method
        Browse the overall Asteroid data-set
        """
        session.params.clear()
        session.params['api_key'] = NASA_API_KEY
        browse_url = f"{NASA_API_URL}{NEO_URL}{BROWSE_ENDPOINT}"
        try:
            response = session.get(browse_url)
            return response.json()
        except Exception as e:
            logger.error(f'Browse unavailable because: {e}')

    ##### BROWSE_PAGINATED #####
    def browse_paginated(self, page=DEFAULT_PAGE, size=DEFAULT_SIZE):
        """
        The docstring for the browse_paginated method
        Browse the overall Asteroid data-set using paginated searches

        :param page: page number of the result set
        :param size: amount of records from the result set
        """
        session.params.clear()
        session.params['page'] = page
        session.params['size'] = size
        session.params['api_key'] = NASA_API_KEY
        browse_paginated_url = f"{NASA_API_URL}{NEO_URL}{BROWSE_ENDPOINT}"
        try:
            response = session.get(browse_paginated_url)
            return response.json()
        except Exception as e:
            logger.error(f'Search unavailable because: {e}')
