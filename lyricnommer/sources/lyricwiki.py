import logging
import requests
import string
from unidecode import unidecode
from bs4 import BeautifulSoup

from ..exceptions import *

log = logging.getLogger(__name__)

def scrape(title, artist):
    """Scrape lyrics from lyrics.wikia.com"""
    # Format artist and title for building url
    title = format(title)
    artist = format(artist)

    # Build url
    url = "http://www.lyrics.wikia.com/{}:{}".format(artist, title)

    # Request url
    try:
        log.debug("Requesting %s", url)
        resp = requests.get(url)
    except requests.ConnectionError as e:
        log.debug("Connection error")
        log.debug(e)
        raise ConnectionError("Couldn't connect to www.lyrics.wikia.com")

    if resp.status_code != 200:
        log.debug("Request failed with %d", resp.status_code)
        return None

    # Parse page
    soup = BeautifulSoup(resp.text, "html.parser")
    lyrics = soup.find("div", "lyricbox")
    if not lyrics:
        log.debug("No lyrics found")
        return None
    
    # Replace br tag with newline
    for br in lyrics.find_all("br"):
        br.replace_with("\n")

    return lyrics.get_text()


def format(url_string):
    """Format artist or title string for building url"""
    url_string = url_string.replace(" ", "_")
    return url_string
