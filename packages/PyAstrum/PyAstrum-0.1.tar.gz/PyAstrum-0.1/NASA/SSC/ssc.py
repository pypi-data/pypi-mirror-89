from NASA import NASA_API_KEY, NASA_API_URL, session
from helpers.log import get_logger

logger = get_logger(__name__)


class SSC(object):
    """
    SSC

    Satellite Situation Center\n
    The Satellite Situation Center Web (SSCWeb) service has been developed
    and is operated jointly by the NASA/GSFC Space Physics Data Facility
    (SPDF) and the National Space Science Data Center (NSSDC) to support a
    range of NASA science programs and to fulfill key international NASA
    responsibilities including those of NSSDC and the World Data Center-A for
    Rockets and Satellites. The software and associated database of SSCWeb
    together form a system to cast geocentric spacecraft location information
    into a framework of (empirical) geophysical regions and mappings of
    spacecraft locations along lines of the Earth's magnetic field. This
    capability is one key to mission science planning (both single missions
    and coordinated observations of multiple spacecraft with ground-based
    investigations) and to subsequent multi-mission data analysis. To get
    started with this API please visit this page.


    https://sscweb.gsfc.nasa.gov/WebServices/REST/
    https://sscweb.gsfc.nasa.gov/WebServices/REST/json/
    """
    pass
