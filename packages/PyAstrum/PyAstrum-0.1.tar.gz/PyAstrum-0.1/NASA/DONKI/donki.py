from NASA import NASA_API_KEY, NASA_API_URL, session
from datetime import datetime as dt, timedelta
from helpers.log import get_logger

logger = get_logger(__name__)

# BASE URL
DONKI_URL = '/DONKI'

# ENDPOINTS
CME_ENDPOINT = '/CME'
CMEA_ENDPOINT = '/CMEAnalysis'
GST_ENDPOINT = '/GST'
IPS_ENDPOINT = '/IPS'
FLR_ENDPOINT = '/FLR'
SEP_ENDPOINT = '/SEP'
MPC_ENDPOINT = '/MPC'
RBE_ENDPOINT = '/RBE'
HSS_ENDPOINT = '/HSS'
WSAES_ENDPOINT = '/WSAEnlilSimulations'
NOTIFICATIONS_ENDPOINT = '/notifications'

# MISCELLANEOUS
ALL = "ALL"
NONE = "NONE"
ZERO = 0
DATE_ISO_FORMAT = "YYYY-MM-DD"
TODAY = dt.utcnow().isoformat()
A_MONTH_AGO = TODAY - timedelta(days=30)


class DONKI(object):
    """
    DONKI

    The Space Weather Database Of Notifications, Knowledge, Information (DONKI)
    is a comprehensive on-line tool for space weather forecasters, scientists,
    and the general space science community.
    DONKI (https://ccmc.gsfc.nasa.gov/donki/) provides chronicles the daily
    interpretations of space weather observations, analysis, models, forecasts,
    and notifications provided by the Space Weather Research Center (SWRC),
    comprehensive knowledge-base search functionality to support anomaly
    resolution and space science research, intelligent linkages, relationships,
    cause-and-effects between space weather activities and comprehensive
    webservice API access to information stored in DONKI.

    This API consists of the following component services:
    - Coronal Mass Ejection (CME)
    - Coronal Mass Ejection (CME) Analysis
    - Geomagnetic Storm (GST)
    - Interplanetary Shock (IPS)
    - Solar Flare (FLR)
    - Solar Energetic Particle (SEP)
    - Magnetopause Crossing (MPC)
    - Radiation Belt Enhancement (RBE)
    - Hight Speed Stream (HSS)
    - WSA+EnlilSimulation
    - Notifications
    """

    @staticmethod
    def get_cme(start_date=TODAY, end_date=A_MONTH_AGO):
        """
        Coronal Mass Ejection (CME)

        :param: startDate: default is 30 days prior to current UTC date
        :param: endDate: default is current UTC date
        """
        session.params.clear()
        session.params['startDate'] = start_date
        session.params['endDate'] = end_date
        session.params['api_key'] = NASA_API_KEY
        cme_url = f"{NASA_API_URL}{DONKI_URL}{CME_ENDPOINT}"
        try: 
            response = session.get(cme_url)
            return response.json()
        except Exception as e:
            logger.error(f'CME unavailable because: {e}')

    @staticmethod
    def get_cmea(start_date=TODAY,
                end_date=A_MONTH_AGO,
                most_accurate_only=True,
                complete_entry_only=True,
                speed=ZERO,
                half_angle=ZERO,
                catalog=ALL,
                keyword=NONE):
        """
        Coronal Mass Ejection (CME) Analysis

        :param: startDate - default is 30 days prior to current UTC date
        :param: endDate - default is current UTC date
        :param: mostAccurateOnly - default is true
        :param: completeEntryOnly - default is true
        :param: speed (lower limit) - default is 0
        :param: halfAngle (lower limit) - default is 0
        :param: catalog - default is ALL (choices: ALL, SWRC_CATALOG,
        JANG_ET_AL_CATALOG)
        :param: keyword - default is NONE (choices: swpc_annex)
        """
        session.params.clear()
        session.params['startDate'] = start_date
        session.params['endDate'] = end_date
        session.params['mostAccurateOnly'] = most_accurate_only
        session.params['completeEntryOnly'] = complete_entry_only
        session.params['speed'] = speed
        session.params['halfAngle'] = half_angle
        session.params['catalog'] = catalog
        session.params['keyword'] = keyword
        session.params['api_key'] = NASA_API_KEY
        cmea_url = f"{NASA_API_URL}{DONKI_URL}{CMEA_ENDPOINT}"
        try:
            response = session.get(cmea_url)
            return response.json()
        except Exception as e:
            logger.error(f'CMEA unavailable because: {e}')

    @staticmethod
    def get_gst(start_date=TODAY, end_date=A_MONTH_AGO):
        """
        Geomagnetic Storm (GST)

        :param: startDate - default is 30 days prior to current UTC date
        :param: endDate - default is current UTC date
        """
        session.params.clear()
        session.params['startDate'] = start_date
        session.params['endDate'] = end_date
        session.params['api_key'] = NASA_API_KEY
        gst_url = f"{NASA_API_URL}{DONKI_URL}{GST_ENDPOINT}"
        try:
            response = session.get(gst_url)
            return response.json()
        except Exception as e:
            logger.error(f'GST unavailable because: {e}')

    @staticmethod
    def get_ips(start_date=TODAY,
                end_date=A_MONTH_AGO,
                location=ALL,
                catalog=ALL):
        """
        Interplanetary Shock (IPS)
        
        :param: startDate - default is 30 days prior to current UTC date
        :param: endDate - default is current UTC date
        :param: location - default is ALL (choices: Earth, MESSENGER, STEREO A,
        STEREO B)
        :param: catalog - default is ALL (choices: SWRC_CATALOG,
        WINSLOW_MESSENGER_ICME_CATALOG)
        """
        session.params.clear()
        session.params['startDate'] = start_date
        session.params['endDate'] = end_date
        session.params['location'] = location
        session.params['catalog'] = catalog
        session.params['api_key'] = NASA_API_KEY
        ips_url = f"{NASA_API_URL}{DONKI_URL}{IPS_ENDPOINT}"
        try:
            response = session.get(ips_url)
            return response.json()
        except Exception as e:
            logger.error(f'IPS unavailable because: {e}')

    @staticmethod
    def get_flr(start_date=TODAY, end_date=A_MONTH_AGO):
        """
        Solar Flare (FLR)
        
        :param: startDate - default is 30 days prior to current UTC date
        :param: endDate - default is current UTC date
        """
        session.params.clear()
        session.params['startDate'] = start_date
        session.params['endDate'] = end_date
        session.params['api_key'] = NASA_API_KEY
        flr_url = f"{NASA_API_URL}{DONKI_URL}{FLR_ENDPOINT}"
        try:
            response = session.get(flr_url)
            return response.json()
        except Exception as e:
            logger.error(f'FLR unavailable because: {e}')

    @staticmethod
    def get_sep(start_date=TODAY, end_date=A_MONTH_AGO):
        """
        Solar Energetic Particle (SEP)

        :param: startDate - default is 30 days prior to current UTC date
        :param: endDate - default is current UTC date
        """
        session.params.clear()
        session.params['startDate'] = start_date
        session.params['endDate'] = end_date
        session.params['api_key'] = NASA_API_KEY
        sep_url = f"{NASA_API_URL}{DONKI_URL}{SEP_ENDPOINT}"
        try:
            response = session.get(sep_url)
            return response.json()
        except Exception as e:
            logger.error(f'SEP unavailable because: {e}')

    @staticmethod
    def get_mpc(start_date=TODAY, end_date=A_MONTH_AGO):
        """
        Magnetopause Crossing (MPC)

        :param: startDate - default is 30 days prior to current UTC date
        :param: endDate - default is current UTC date
        """
        session.params.clear()
        session.params['startDate'] = start_date
        session.params['endDate'] = end_date
        session.params['api_key'] = NASA_API_KEY
        mpc_url = f"{NASA_API_URL}{DONKI_URL}{MPC_ENDPOINT}"
        try:
            response = session.get(mpc_url)
            return response.json()
        except Exception as e:
            logger.error(f'MPC unavailable because: {e}')

    @staticmethod
    def get_rbe(start_date=TODAY, end_date=A_MONTH_AGO):
        """
        Radiation Belt Enhancement (RBE)

        :param: startDate - default is 30 days prior to current UTC date
        :param: endDate - default is current UTC date
        """
        session.params.clear()
        session.params['startDate'] = start_date
        session.params['endDate'] = end_date
        session.params['api_key'] = NASA_API_KEY
        rbe_url = f"{NASA_API_URL}{DONKI_URL}{RBE_ENDPOINT}"
        try:
            response = session.get(rbe_url)
            return response.json()
        except Exception as e:
            logger.error(f'RBE unavailable because: {e}')

    @staticmethod
    def get_hss(start_date=TODAY, end_date=A_MONTH_AGO):
        """
        Hight Speed Stream (HSS)

        :param: startDate - default is 30 days prior to current UTC date
        :param: endDate - default is current UTC date
        """
        session.params.clear()
        session.params['startDate'] = start_date
        session.params['endDate'] = end_date
        session.params['api_key'] = NASA_API_KEY
        hss_url = f"{NASA_API_URL}{DONKI_URL}{HSS_ENDPOINT}"
        try:
            response = session.get(hss_url)
            return response.json()
        except Exception as e:
            logger.error(f'HSS unavailable because: {e}')

    @staticmethod
    def get_wsa_enlilsimulation(start_date=TODAY, end_date=A_MONTH_AGO):
        """
        WSA+EnlilSimulation

        :param: startDate - default is 30 days prior to current UTC date
        :param: endDate - default is current UTC date
        """
        session.params.clear()
        session.params['startDate'] = start_date
        session.params['endDate'] = end_date
        session.params['api_key'] = NASA_API_KEY
        wsa_enlilsimulation = f"{NASA_API_URL}{DONKI_URL}{WSAES_ENDPOINT}"
        try:
            response = session.get(wsa_enlilsimulation)
            return response.json()
        except Exception as e:
            logger.error(f'WSA+EnlilSimulation unavailable because: {e}')

    @staticmethod
    def get_notifications(start_date=TODAY, end_date=A_MONTH_AGO, type="all"):
        """
        Notifications

        Note:
        The request date range is limit to 30 days. If the request range is
        greater than 30 days, it would limit your request range to (endDate-30)
        to endDate.

        :param: startDate - default is 7 days prior to current UTC date
        :param: endDate - default is current UTC date
        :param: type - default is all (choices: FLR, SEP, CME, IPS, MPC, GST,
        RBE, report)
        """
        session.params.clear()
        session.params['startDate'] = start_date
        session.params['endDate'] = end_date
        session.params['type'] = type
        session.params['api_key'] = NASA_API_KEY
        notifications_url = f"{NASA_API_URL}{DONKI_URL}\
                                {NOTIFICATIONS_ENDPOINT}"
        try:
            response = session.get(notifications_url)
            return response.json()
        except Exception as e:
            logger.error(f'Notifications unavailable because: {e}')
