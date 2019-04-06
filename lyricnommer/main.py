import sys
import argparse
import logging
import filetype
from pathlib import Path
from . import tag

supported_types = ['mp3']

def main():
    # Parse user input
    parser = parse_args(sys.argv[1:])

    # Check that specified path is valid
    p = Path(parser.path)
    if not p.is_dir():
        sys.exit('Error: Invalid path')

    # Grab all files in directory and subdirectories
    files = (f for f in p.glob('**/*') if f.is_file())

    # Check and tag each file
    for file_path in files:
        kind = filetype.guess(str(file_path))

        if kind is None or kind.mime[0:6] != "audio/":
            # Ignore non audio files
            pass

        elif not kind.extension in supported_types:
            # Warn user of unsupported file type
            print ("Unsupported file type '" + kind.extension + "' (" + file_path.name + ")")

        else:
            if parser.force:
                tag.delete_lyrics(file_path, kind.extension)
            tag.add_lyrics(file_path, kind.extension)


# Parse user input
def parse_args(args):
    parser = argparse.ArgumentParser(
    description="""A command line tool to add lyrics to music files.
                    Supported file types: {}.""".format(", ".join(supported_types)))
    parser.add_argument('path', help='path of the directory to be tagged')
    parser.add_argument('-f', '--force', action='store_true', help='overwrite existing lyrics')

    return parser.parse_args(args)