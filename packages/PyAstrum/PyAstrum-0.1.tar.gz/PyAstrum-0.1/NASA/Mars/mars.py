from NASA import NASA_API_KEY, NASA_API_URL, session
from datetime import datetime as dt
from helpers.log import get_logger

logger = get_logger(__name__)

# BASE URLs
MARS_URL = "mars-photos/api/v1/"
MANIFESTS = "manifests/"
CURIOSITY_ENDPOINT = 'rovers/curiosity/photos'
OPPORTUNITY_ENDPOINT = 'rovers/opportunity/photos'
SPIRIT_ENDPOINT = 'rovers/spirit/photos'

# ROVERS
CURIOSITY = 'curiosity'
OPPORTUNITY = 'opportunity'
SPIRIT = 'spirit'

# CAMERAS
FHAZ = "FHAZ"
RHAZ = "RHAZ"
MAST = "MAST"
CHEMCAM = "CHEMCAM"
MAHLI = "MAHLI"
MARDI = "MARDI"
NAVCAM = "NAVCAM"
PANCAM = "PANCAM"
MINITES = "MINITES"

# MISCELLANEOUS
DEFAULT_PAGE = 1
DEFAULT_SOL = 0
DATE_ISO_FORMAT = "YYYY-MM-DD"
TODAY = dt.utcnow().isoformat()


class MARS(object):
    """
    MARS

    This API is designed to collect image data gathered by NASA's Curiosity,
    Opportunity, and Spirit rovers on Mars and make it more easily available
    to other developers, educators, and citizen scientists. This API is
    maintained by Chris Cerami (https://github.com/chrisccerami/mars-photo-api).

    Each rover has its own set of photos stored in the database, which can be
    queried separately. There are several possible queries that can be made
    against the API. Photos are organized by the sol (Martian rotation or
    day) on which they were taken, counting up from the rover's landing date.
    A photo taken on Curiosity's 1000th Martian sol exploring Mars, for
    example, will have a sol attribute of 1000. If instead you prefer to
    search by the Earth date on which a photo was taken, you can do that too.

    Along with querying by date, results can also be filtered by the camera
    with which it was taken and responses will be limited to 25 photos per
    call. Queries that should return more than 25 photos will be split onto
    several pages, which can be accessed by adding a 'page' param to the
    query.


    ### Rover Cameras

    Abbreviation |           Camera           | Curiosity | Opportunity | Spirit
    FHAZ	     Front Hazard Avoidance Camera      ✔	        ✔	        ✔
    RHAZ	     Rear Hazard Avoidance Camera	    ✔	        ✔	        ✔
    MAST	     Mast Camera	                    ✔		
    CHEMCAM	     Chemistry and Camera Complex	    ✔		
    MAHLI	     Mars Hand Lens Imager	            ✔		
    MARDI	     Mars Descent Imager	            ✔		
    NAVCAM	     Navigation Camera	                ✔	        ✔	        ✔
    PANCAM	     Panoramic Camera		                        ✔	        ✔
    MINITES	 Miniature Thermal Emission Spectrometer (Mini-TES)	✔	        ✔


    #### Querying by Martian sol

    Parameter   |   Type  | Default |       Description
    sol	        |   int   | none    | sol (ranges from 0 to MAX)
    camera	    |  string |	all	    | see table abbreviations
    page	    |   int   |	1       | 25 items per page returned


    #### Querying by Earth date

    Parameter   |   Type   | Default |       Description
    earth_date	|YYYY-MM-DD| none    | date on earth for the given sol
    camera	    |  string  | all     | see table abbreviations
    page	    |   int    | 1       | 25 items per page returned
    """
    
    @staticmethod
    def get_mission_manifest_for(rover=CURIOSITY):
        """
        Get mission's manifest for the given rover
        """
        session.params.clear()
        session.params['api_key'] = NASA_API_KEY
        manifests_url = f"{NASA_API_URL}{MARS_URL}{MANIFESTS}{rover}"
        try:
            response = session.get(manifests_url)
            return response.json()
        except Exception as e:
            logger.error(f'Manifest unavailable because: {e}')

    @staticmethod
    def get_curiosity_photos_on_martian_sol(sol=DEFAULT_SOL,
                                            camera=FHAZ,
                                            page=DEFAULT_PAGE):
        """
        Get Curiosity's photos for the specified sol, camera, and page
        """
        session.params.clear()
        session.params['sol'] = sol
        session.params['camera'] = camera
        session.params['page'] = page
        session.params['api_key'] = NASA_API_KEY
        martian_sol_photos_url = f"{NASA_API_URL}{MARS_URL}\
                                    {CURIOSITY_ENDPOINT}"
        try:
            response = session.get(martian_sol_photos_url)
            return response.json()
        except Exception as e:
            logger.error(f'Photos unavailable because: {e}')

    @staticmethod
    def get_curiosity_photos_on_earth_date(date=TODAY,
                                            camera=FHAZ,
                                            page=DEFAULT_PAGE):
        """
        Get Curiosity's photos for the specified earth date, camera, and page
        """
        session.params.clear()
        session.params['earth_date'] = date
        session.params['camera'] = camera
        session.params['page'] = page
        session.params['api_key'] = NASA_API_KEY
        earth_date_photos_url = f"{NASA_API_URL}{MARS_URL}\
                                    {CURIOSITY_ENDPOINT}"
        try:
            response = session.get(earth_date_photos_url)
            return response.json()
        except Exception as e:
            logger.error(f'Photos unavailable because: {e}')
    
    @staticmethod
    def get_opportunity_photos_on_martian_sol(sol=DEFAULT_SOL,
                                                camera=FHAZ,
                                                page=DEFAULT_PAGE):
        """
        Get Opportunity's photos for the specified sol, camera, and page
        """
        session.params.clear()
        session.params['sol'] = sol
        session.params['camera'] = camera
        session.params['page'] = page
        session.params['api_key'] = NASA_API_KEY
        martian_sol_photos_url = f"{NASA_API_URL}{MARS_URL}\
                                    {OPPORTUNITY_ENDPOINT}"
        try:
            response = session.get(martian_sol_photos_url)
            return response.json()
        except Exception as e:
            logger.error(f'Photos unavailable because: {e}')

    @staticmethod
    def get_opportunity_photos_on_earth_date(date=TODAY,
                                                camera=FHAZ,
                                                page=DEFAULT_PAGE):
        """
        Get Opportunity's photos for the specified earth date, camera, and page
        """
        session.params.clear()
        session.params['earth_date'] = date
        session.params['camera'] = camera
        session.params['page'] = page
        session.params['api_key'] = NASA_API_KEY
        earth_date_photos_url = f"{NASA_API_URL}{MARS_URL}\
                                    {OPPORTUNITY_ENDPOINT}"
        try:
            response = session.get(earth_date_photos_url)
            return response.json()
        except Exception as e:
            logger.error(f'Photos unavailable because: {e}')
    
    @staticmethod
    def get_spirit_photos_on_martian_sol(sol=DEFAULT_SOL,
                                            camera=FHAZ,
                                            page=DEFAULT_PAGE):
        """
        Get Spirit's photos for the specified sol, camera, and page
        """
        session.params.clear()
        session.params['sol'] = sol
        session.params['camera'] = camera
        session.params['page'] = page
        session.params['api_key'] = NASA_API_KEY
        martian_sol_photos_url = f"{NASA_API_URL}{MARS_URL}\
                                    {SPIRIT_ENDPOINT}"
        try:
            response = session.get(martian_sol_photos_url)
            return response.json()
        except Exception as e:
            logger.error(f'Photos unavailable because: {e}')

    @staticmethod
    def get_spirit_photos_on_earth_date(date=TODAY,
                                        camera=FHAZ,
                                        page=DEFAULT_PAGE):
        """
        Get Spirit's photos for the specified earth date, camera, and page
        """
        session.params.clear()
        session.params['earth_date'] = date
        session.params['camera'] = camera
        session.params['page'] = page
        session.params['api_key'] = NASA_API_KEY
        earth_date_photos_url = f"{NASA_API_URL}{MARS_URL}\
                                    {SPIRIT_ENDPOINT}"
        try:
            response = session.get(earth_date_photos_url)
            return response.json()
        except Exception as e:
            logger.error(f'Photos unavailable because: {e}')
