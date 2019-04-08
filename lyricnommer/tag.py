import logging
import mutagen
from mutagen.id3 import ID3, USLT
from mutagen.id3 import ID3NoHeaderError

from .exceptions import *
from .sources import *

log = logging.getLogger(__name__)
sources = (metrolyrics, lyricwiki, genius)

def add_lyrics(file_path, kind):
    """Add lyric tag to file"""
    if kind == "mp3":
        audio = ID3(file_path)
        if not audio.getall("USLT"):
            title = str(audio.get('TIT2'))
            artist = str(audio.get('TPE1'))

            try:
                lyrics = get_lyrics(title, artist)
            except Exception:
                raise
            else:
                log.debug("Adding lyrics")
                audio.add(USLT(encoding=3, lang="eng", text=lyrics))
                audio.save()

        else:
            raise ExistingLyricsError()

def delete_lyrics(file_path, kind, strings):
    """Delete lyric tags from file"""
    if kind == "mp3":
        audio = ID3(file_path)
        
        # Delete lyrics if no strings given
        if not strings:
            audio.delall("USLT")
            audio.save()

        # Delete lyrics if it contains any given string
        for s in strings:
            for frame in audio.getall("USLT"):
                if s.lower() in str(frame).lower():
                    audio.delall("USLT")
                    audio.save()
                    return

def get_lyrics(title, artist):
    """Try to get lyrics from different sources"""
    for src in sources:
        try:
            lyrics = src.scrape(title, artist)
        except Exception:
            raise
            
        if lyrics:
            return lyrics

    raise LyricsNotFoundError()  

