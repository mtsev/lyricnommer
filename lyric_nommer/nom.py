#!/usr/bin/env python3

import sys
import argparse
import logging

from pathlib import Path

from mutagen.id3 import ID3, USLT
from mutagen.id3 import ID3NoHeaderError

# Check for correct input from user
if len(sys.argv) != 2: 
    sys.exit('Usage: ./nom <path>')

# Check that specified path is valid
p = Path(sys.argv[1])
if not p.is_dir():
    sys.exit('Error: Invalid path')

# Iterate through files and tag
for file_path in p.glob('**/*'):
    if (file_path.is_file()):
        try:
            audio = ID3(file_path)
            title = audio.get('TIT2')
            artist = audio.get('TPE1')

#            audio.add(USLT(encoding=3, lang="eng", desc="desc", text="lorem ipsum"))
#            audio.save()

            print("USLT::\t\t", audio.get('USLT::'))
            print("USLT::eng\t", audio.get('USLT::eng'))
            print('USLT:desc:eng\t', audio.get('USLT:desc:eng'))
            print('USLT:None:eng\t', audio.get('USLT:None:eng'))

            print(f'{file_path.name} is {title} by {artist}')
        except ID3NoHeaderError:
#            print(f'Couldn\'t tag \"{file_path.name}\" (unsupported file type)')
            pass
        


