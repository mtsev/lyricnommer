import sys
import argparse
import logging
import filetype
from pathlib import Path

from .exceptions import *
from . import tag

supported_types = ['mp3']
tagged = []
unsupported = []
existing = []
notfound = []

def main():
    """Main"""
    # Parse user input
    parser = parse_args(sys.argv[1:])

    # Check that specified path is valid
    p = Path(parser.path)
    if not p.is_dir():
        sys.exit('nom.py: error: invalid path')

    # Set up logger based on flags
    log = log_setup(parser)
    log.debug("\033[91mDEBUG has been set\033[0m")

    # Grab all files in directory and subdirectories
    files = (f for f in p.glob('**/*') if f.is_file())

    # Check and tag each file
    for file_path in files:
        kind = filetype.guess(str(file_path))

        if kind is None or kind.mime[0:6] != "audio/":
            # Ignore non audio files
            pass

        elif not kind.extension in supported_types:
            # Unsupported file type
            unsupported.append((file_path.relative_to(p), kind.extension))

        else:
            # Tags away!
            try:
                if parser.force:
                    tag.delete_lyrics(file_path, kind.extension)
                tag.add_lyrics(file_path, kind.extension)

            except LyricsNotFoundError:
                notfound.append(file_path.relative_to(p))

            except ExistingLyricsError:
                existing.append(file_path.relative_to(p))

            else:
                tagged.append(file_path.relative_to(p))

    # Print number of files tagged
    if tagged:
        log.warning("Successfully added lyrics to %d files", len(tagged))
        log.info('')

    # Print error for lyrics not found
    if notfound:
        log.warning("Lyrics not found for %d files", len(notfound))
        for f in notfound:
            log.info(f)
        log.info('')

    # Print error for existing lyrics on file
    if existing:
        log.warning("Existing lyrics on %d files", len(existing))
        for f in existing:
            log.info(f)
        log.info('')

    # Print error for unsupported file type
    if unsupported:
        log.info("Unsupported file type for %d files", len(unsupported))
        for f in unsupported:
            log.info(str(f[0]) + " (" + f[1] + ")")
        log.info('')

def parse_args(args):
    """Parse user input"""
    parser = argparse.ArgumentParser(
    description="""A command line tool to add lyrics to music files.
                    Supported file types: {}.""".format(", ".join(supported_types)))
    parser.add_argument('path', help='path of the directory to be tagged')
    parser.add_argument('-f', '--force', action='store_true', help='overwrite existing lyrics')
    parser.add_argument('-v', '--verbose', action='store_true', help='list the files that failed')
    parser.add_argument('--debug', action='store_true', help=argparse.SUPPRESS)

    return parser.parse_args(args)

def log_setup(parser):
    """Set up logger to print to user"""
    # Create logger
    log = logging.getLogger(__package__)
    
    # Set level from options
    if parser.debug:
        log.setLevel(logging.DEBUG)
    elif parser.verbose:
        log.setLevel(logging.INFO)
    else:
        log.setLevel(logging.WARNING)

    # Set output format
    formatter = logging.Formatter("%(message)s")
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(formatter)
    log.addHandler(handler)

    return log