#!/usr/bin/env python3

import sys
import argparse
import logging

from pathlib import Path

from mutagen.id3 import ID3, USLT
from mutagen.id3 import ID3NoHeaderError

from scrape import *

def main():
    # Check for correct input from user
    if len(sys.argv) != 2: 
        sys.exit('Usage: ./nom <path>')

    # Check that specified path is valid
    p = Path(sys.argv[1])
    if not p.is_dir():
        sys.exit('Error: Invalid path')

    # Iterate through files and tag
    for file_path in p.glob('**/*'):
        if file_path.is_file():
            try:
                audio = ID3(file_path)

                # Check for existing USLT frame
                # Assumes desc="" and lang="eng"
                if audio.get('USLT::eng') is None:

                    title = str(audio.get('TIT2'))
                    artist = str(audio.get('TPE1'))
                    lyrics = get_lyrics(title, artist)

                    if lyrics:
                        audio.add(USLT(encoding=3, lang="eng", text=lyrics))
                        audio.save()
                        print("\033[32mLyrics added to \"" + file_path.name + "\"\033[0m")
                        print("================================================================")
                        print(lyrics)
                        print("================================================================")
                        print()
                    else:
                        print("\033[31mCouldn't find lyrics for \"" + file_path.name  + "\"\033[0m")

                else:
                    print("\033[33mExisting lyrics on \"" + file_path.name + "\"\033[0m")

            except ID3NoHeaderError:
                print("\033[31mCouldn't tag \"" + file_path.name + "\" (unsupported file type)\033[0m")


# Tries to get lyrics from different sources
def get_lyrics(title, artist):
    lyrics = scrape_metrolyrics(title, artist)
    if not lyrics:
        lyrics = scrape_darklyrics(title, artist)
    return lyrics


if __name__ == '__main__':
    main()

