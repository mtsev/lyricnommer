import logging
import requests
import string
from unidecode import unidecode
from bs4 import BeautifulSoup

from ..exceptions import *

log = logging.getLogger(__name__)


def scrape(title, artist):
    """Scrape lyrics from genius.com"""
    # Format artist and title for building url
    title = format(title)
    artist = format(artist)

    # Build url
    url = "http://genius.com/{}-{}-lyrics".format(artist, title)

    # Request url
    try:
        log.debug("Requesting %s", url)
        resp = requests.get(url)
    except requests.ConnectionError as e:
        log.debug("Connection error")
        log.debug(e)
        raise ConnectionError("Couldn't connect to genius.com")

    if resp.status_code != 200:
        log.debug("Request failed with %d", resp.status_code)
        return None

    # Parse page
    soup = BeautifulSoup(resp.text, "html.parser")
    lyrics = soup.find("div", "lyrics")
    if not lyrics:
        log.debug("No lyrics found")
        return None

    return lyrics.get_text()


def format(url_string):
    """Format artist or title string for building url"""
    url_string = url_string.replace("+", "and")
    url_string = unidecode(url_string)
    url_string = url_string.translate(str.maketrans('', '', string.punctuation))
    url_string = ' '.join(url_string.split())
    url_string = url_string.replace(" ", "-")
    return url_string
