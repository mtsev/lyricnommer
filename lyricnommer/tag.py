import logging
import mutagen
from mutagen.id3 import ID3, USLT
from mutagen.id3 import ID3NoHeaderError

from .exceptions import *
from .sources import *

log = logging.getLogger(__name__)

# Get lyrics from metrolyrics.com
def scrape_metrolyrics(title, artist):
    if not (title and artist):
        return ""

    parser = metrolyrics.Parser(artist, title)
    try:
        lyrics = parser.parse()
    except Exception as e:
        log.debug("Error in metrolyrics parser")
        log.debug(str(e))
        return ""

    return lyrics


# Get lyrics from darklyrics.com
def scrape_darklyrics(title, artist):
    if not (title and artist):
        return ""

    parser = darklyrics.Parser(artist, title)
    try:
        lyrics = parser.parse()
    except Exception as e:
        log.debug("Error in darklyrics parser")
        log.debug(str(e))
        return ""

    return lyrics


def add_lyrics(file_path, kind):
    """Add lyric tag to file"""
    if kind == "mp3":
        audio = ID3(file_path)
        if not audio.getall("USLT"):
            title = str(audio.get('TIT2'))
            artist = str(audio.get('TPE1'))
            lyrics = get_lyrics(title, artist)

            if lyrics:
                audio.add(USLT(encoding=3, lang="eng", text=lyrics))
                audio.save()

            else:
                raise LyricsNotFoundError()

        else:
            raise ExistingLyricsError()


def delete_lyrics(file_path, kind):
    """Delete lyric tags from file"""
    if kind == "mp3":
        audio = ID3(file_path)
        audio.delall("USLT")
        audio.save()


# Tries to get lyrics from different sources
def get_lyrics(title, artist):
    lyrics = scrape_metrolyrics(title, artist)
    if not lyrics:
        lyrics = scrape_darklyrics(title, artist)
    return lyrics


