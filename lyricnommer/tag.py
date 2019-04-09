import logging
import mutagen
from mutagen.id3 import ID3, USLT
from mutagen._vorbis import VCommentDict as Vorbis

from .exceptions import *
from .sources import *

sources = (metrolyrics, lyricwiki, genius)
log = logging.getLogger(__name__)


def add_lyrics(file_path):
    """Add lyric tag to file"""
    audio = mutagen.File(file_path)
    try:
        tags = audio.tags
    except AttributeError:
        raise UnknownTypeError()

    else:
        if isinstance(tags, ID3):
            if tags.getall("USLT"):
                raise ExistingLyricsError()
            elif not (tags.get('TIT2') and tags.get('TPE1')):
                log.debug("Title or Artist missing")
                raise LyricsNotFoundError()
            else:
                lyrics = get_lyrics(tags.get('TIT2'), tags.get('TPE1'))
                log.debug("Adding lyrics")
                tags.add(USLT(encoding=3, text=lyrics))
                tags.save(file_path)
                
        elif isinstance(tags, Vorbis):
            if 'LYRICS' in tags:
                raise ExistingLyricsError()
            elif ('TITLE' not in tags) or ('ARTIST' not in tags):
                log.debug("Title or Artist missing")
                raise LyricsNotFoundError()
            else:
                lyrics = get_lyrics(tags['TITLE'][0], tags['ARTIST'][0])
                log.debug("Adding lyrics")
                tags['LYRICS'] = lyrics
                audio.save(file_path) 

        else:
            raise UnsupportedTypeError(audio.mime[0][6:])


def delete_lyrics(file_path, strings):
    """Delete lyric tags from file"""
    audio = mutagen.File(file_path)
    try:
        tags = audio.tags
    except AttributeError:
        raise UnknownTypeError()

    else:
        if isinstance(tags, ID3):
            # Delete lyrics if no strings given
            if not strings:
                tags.delall("USLT")
                tags.save(file_path)

            # Delete lyrics if it contains any given string
            for s in strings:
                for frame in tags.getall("USLT"):
                    if s.lower() in str(frame).lower():
                        tags.delall("USLT")
                        tags.save(file_path)
                        return

        elif isinstance(tags, Vorbis):
            # No action needed if no lyrics exist
            if 'LYRICS' not in tags:
                return

            # Delete lyrics if no strings given
            if not strings:
                del tags['LYRICS']
                audio.save(file_path)

            # Delete lyrics if it contains any given string
            for s in strings:
                for frame in tags['LYRICS']:
                    if s.lower() in str(frame).lower():
                        del tags['LYRICS']
                        audio.save(file_path)
                        return

        else:
            raise UnsupportedTypeError(audio.mime[0][6:])


def get_lyrics(title, artist):
    """Try to get lyrics from different sources"""
    connections = len(sources)
    for src in sources:
        try:
            lyrics = src.scrape(str(title), str(artist))
            if lyrics:
                return lyrics

        # Pass up exception if we couldn't connect to any sources
        except ConnectionError as e:
            log.debug(str(e))
            connections -= 1
            if not connections:
                raise

    raise LyricsNotFoundError()
