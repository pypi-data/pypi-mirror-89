from NASA import session
from helpers.log import get_logger

logger = get_logger(__name__)

# BASE URLS
CALTECH_URL = "https://exoplanetarchive.ipac.caltech.edu"
EXOPLANET_URL = f"{CALTECH_URL}/cgi-bin/nstedAPI/nph-nstedAPI"

# QUERIES CONDITIONS
ALL = "where=*"
CAMPAIGN_9 = "where=k2_campaign=9"
CANDIDATES_SMALLER_2RE_EQUILIBRIUM_TEMP = """where=koi_prad<2 and koi_teq>180
    and koi_teq<303 and koi_disposition like 'CANDIDATE'
    """
EXOPLANETS = "table=exoplanets"
FOUND_BY_TESS = "where=pl_facility like '%25TESS%25'"
JSON = "format=json"
K2_TARGETS = "table=k2targets"
KEPLER = "where=pl_kepflag=1"
KNOWN_STARS = "select=distinct pl_hostname&order=pl_hostname"
KOI = "table=koi"
LIST = "table=cumulative"
MICROLENSING = "where=pl_discmethod like 'Microlensing' and st_nts > 0"
CONFIRMED_MISSION_STAR = "table=missionstars&where=st_ppnum>0"
NON_CONFIRMED = "where=koi_disposition like 'CANDIDATE'"
PLANETS = "select=pl_hostname,ra,dec"
TRANSITING = "where=pl_tranflag=1"


class EXOPLANET(object):
    """
    EXOPLANET

    The Exoplanet Archive API allows programatic access to NASA's Exoplanet
    Archive database. This API contains a ton of options so to get started
    please visit this page for introductory materials. To see what data is
    available in this API visit  and also be sure to check out
    best-practices and troubleshooting in case you get stuck.

    EXOPLANET Archive: {CALTECH_URL}/index.html\n
    API Available data: {CALTECH_URL}/docs/program_interfaces.html#data\n
    IPAC: Infrared Processing and Analysis Center: http://www.ipac.caltech.edu/\n
    NexScI: NASA Exoplanet Science Institute: http://nexsci.caltech.edu/\n
    CalTech: California Institute of Technology: http://www.caltech.edu/\n

    This research has made use of the NASA Exoplanet Archive, which is
    operated by the California Institute of Technology, under contract with
    the National Aeronautics and Space Administration under the Exoplanet
    Exploration Program.

    Happy planet hunting!         
    """

    @staticmethod
    def get_all_confirmed_exoplanets(format=JSON):
        """
        All confirmed exoplanets
        """
        session.params.clear()
        all_confirmed_exoplanets = f"{EXOPLANET_URL}?{EXOPLANETS}&{ALL}&\
                                        {format}"
        try:
            response = session.get(all_confirmed_exoplanets)
            return response.json()
        except Exception as e:
            logger.error(f'Exoplanets unavailable because: {e}')

    @staticmethod
    def get_confirmed_exoplanets_in_kepler_field(format=JSON):
        """
        Confirmed exoplanets in Kepler field
        """
        session.params.clear()
        exoplanets_in_kepler_field = f"{EXOPLANET_URL}?{EXOPLANETS}&\
                                        {KEPLER}&{format}" 
        try:
            response = session.get(exoplanets_in_kepler_field)
            return response.json()
        except Exception as e:
            logger.error(f'Exoplanets unavailable because: {e}')

    @staticmethod
    def get_confirmed_exoplanets_transiting_host_star(format=JSON):
        """
        Confirmed exoplanets that transit their host stars
        """
        session.params.clear()
        exoplanets_transiting_host_star = f"{EXOPLANET_URL}?{EXOPLANETS}&\
                                            {TRANSITING}&{format}"
        try:
            response = session.get(exoplanets_transiting_host_star)
            return response.json()
        except Exception as e:
            logger.error(f'Exoplanets unavailable because: {e}')

    @staticmethod
    def get_confirmed_exoplanets_in_mission_star(format=JSON):
        """
        Confirmed exoplanets in the Mission Star list
        """
        session.params.clear()
        exoplanets_in_mission_star = f"{EXOPLANET_URL}?\
                                        {CONFIRMED_MISSION_STAR}&{format}"
        try:
            response = session.get(exoplanets_in_mission_star)
            return response.json()
        except Exception as e:
            logger.error(f'Exoplanets unavailable because: {e}')

    @staticmethod
    def get_confirmed_exoplanets_found_by_tess(format=JSON):
        """
        All confirmed exoplanets found by TESS
        """
        session.params.clear()
        exoplanets_found_by_tess = f"{EXOPLANET_URL}?{EXOPLANETS}&{PLANETS}&\
                                        {FOUND_BY_TESS}&{format}"
        try:
            response = session.get(exoplanets_found_by_tess)
            return response.json()
        except Exception as e:
            logger.error(f'Exoplanets unavailable because: {e}')

    @staticmethod
    def get_all_koi(format=JSON):
        """
        Get all KOI
        """
        session.params.clear()
        all_koi = f"{EXOPLANET_URL}?{KOI}&{ALL}&{format}"
        try:
            response = session.get(all_koi)
            return response.json()
        except Exception as e:
            logger.error(f'KOIs unavailable because: {e}')

    @staticmethod
    def get_non_confirmed_exoplanet_candidates(format=JSON):
        """
        List of non-confirmed exoplanet candidates
        """
        session.params.clear()
        non_confirmed_exoplanet_candidates = f"{EXOPLANET_URL}?{LIST}&\
                                                {NON_CONFIRMED}&{format}"
        try:
            response = session.get(non_confirmed_exoplanet_candidates)
            return response.json()
        except Exception as e:
            logger.error(f'Exoplanet candidates unavailable because: {e}')

    @staticmethod
    def get_candidates_smaller_than_2re_equilibrium_temp(format=JSON):
        """
        All planetary candidates smaller than 2Re with equilibrium
        temperatures between 180-303K
        """
        session.params.clear()
        candidates = f"{EXOPLANET_URL}?{LIST}&\
                        {CANDIDATES_SMALLER_2RE_EQUILIBRIUM_TEMP}&\
                        {format}"
        try:
            response = session.get(candidates)
            return response.json()
        except Exception as e:
            logger.error(f'Candidates unavailable because: {e}')

    @staticmethod
    def get_K2_targets_from_campaign_9(format=JSON):
        """
        K2 targets from campaign 9
        """
        session.params.clear()
        k2_targets_from_campaign_9 = f"{EXOPLANET_URL}?{K2_TARGETS}&\
                                        {CAMPAIGN_9}&{format}"
        try:
            response = session.get(k2_targets_from_campaign_9)
            return response.json()
        except Exception as e:
            logger.error(f'Exoplanets unavailable because: {e}')

    @staticmethod
    def get_known_stars_to_host_exoplanets(format=JSON):
        """
        Stars known to host exoplanets listed in ascending order
        """
        session.params.clear()
        known_stars_to_host_exoplanets = f"{EXOPLANET_URL}?{EXOPLANETS}&\
                                            {KNOWN_STARS}&{format}"
        try:
            response = session.get(known_stars_to_host_exoplanets)
            return response.json()
        except Exception as e:
            logger.error(f'Stars unavailable because: {e}')

    @staticmethod
    def get_microlensing_planets_with_time_series(format=JSON):
        """
        All microlensing planets with time series
        """
        session.params.clear()
        microlensing_planets_with_time_series = f"{EXOPLANET_URL}?\
                                                    {EXOPLANETS}&\
                                                    {MICROLENSING}&\
                                                    {format}"
        try:
            response = session.get(microlensing_planets_with_time_series)
            return response.json()
        except Exception as e:
            logger.error(f'Exoplanets unavailable because: {e}')
