import logging
import requests
import string
from unidecode import unidecode
from bs4 import BeautifulSoup

from ..exceptions import *

log = logging.getLogger(__name__)
#import sys
#logging.basicConfig(stream=sys.stdout,level=logging.DEBUG)

def scrape(title, artist):
    """Scrape lyrics from metrolyrics.com"""
    # Format artist and title for building url
    title = format(title)
    artist = format(artist)

    # Build url
    url = "http://www.metrolyrics.com/{}-lyrics-{}.html".format(title, artist)

    # Request url
    try:
        log.debug("Requesting %s", url)
        resp = requests.get(url)
    except requests.ConnectionError as e:
        log.debug("Connection error")
        log.debug(e)
        raise ConnectionError("Couldn't connect to www.metrolyrics.com")

    if resp.status_code != 200:
        log.debug("Request failed with %d", resp.status_code)
        return None

    # Parse page
    soup = BeautifulSoup(resp.text, "html.parser")
    verses = [ v.get_text() for v in soup.find_all("p", "verse") ]
    if not verses:
        log.debug("No verses found")
        return None
  
    return ("\n\n".join(verses))


def format(url_string):
    """Format artist or title string for building url"""
    url_string = url_string.replace("+", "and")
    url_string = unidecode(url_string)
    url_string = url_string.translate(str.maketrans('', '', string.punctuation))
    url_string = ' '.join(url_string.split())
    url_string = url_string.replace(" ", "-")
    return url_string