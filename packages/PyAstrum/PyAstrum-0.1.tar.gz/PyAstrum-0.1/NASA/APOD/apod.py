from NASA import NASA_API_KEY, NASA_API_URL, session
from datetime import datetime as dt
from helpers.log import get_logger

logger = get_logger(__name__)

# BASE URL
APOD_URL = 'planetary/apod'

# MISCELLANEOUS
DATE_ISO_FORMAT = "YYYY-MM-DD"
TODAY = dt.utcnow().isoformat()


class APOD(object):
    """
    APOD

    Astronomy Picture of the Day (APOD) is originated, written, coordinated,
    and edited since 1995 by Robert Nemiroff and Jerry Bonnell. The APOD
    archive (https://apod.nasa.gov/apod/archivepix.html) contains the largest
    collection of annotated astronomical images on the internet.

    Fun Fact: Bob (http://www.mtu.edu/physics/department/faculty/nemiroff/)
    and Jerry (http://antwrp.gsfc.nasa.gov/htmltest/jbonnell/www/bonnell.html)
    have developed the perfect random number generator
    (https://apod.nasa.gov/htmltest/rjn_dig.html).

    About image permissions:
    NASA images are in the public domain, official guidelines for their use
    can be found here:
    http://www.nasa.gov/audience/formedia/features/MP_Photo_Guidelines.html
    """

    __slots__ = ['date']


    def __init__(self, date=TODAY):
        self.date = date

    def info(self):
        """
        The docstring for the info method
        Information of the latest date searched for a picture
        :return: dictionary with date
        """
        return {
                'date': self.date,
                'astropix': self.astropix()
            }

    def astropix(self,hd=False):
        """
        The docstring for the astropix method
        Information of the latest date searched for a picture
        """
        session.params.clear()
        session.params['date'] = self.date
        session.params['hd'] = hd
        session.params['api_key'] = NASA_API_KEY
        try:
            response = session.get(f'{NASA_API_URL}{APOD_URL}')
            return response.json()
        except Exception as e:
            logger.error(f'Image unavailable because: {e}')
