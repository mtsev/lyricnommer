import sys
import argparse
import logging
from pathlib import Path

from .exceptions import *
from . import tag

supported_types = ('MP3', 'FLAC', 'Ogg', 'AIFF')
unsupported = []
existing = []
notfound = []
invalid = []

log = logging.getLogger(__package__)


def main():
    """Main"""
    # Parse user input
    parser = parse_args(sys.argv[1:])
    parser.no_bar |= parser.debug

    # Set up logger based on flags
    log_setup(parser)
    log.debug("\033[31mDEBUG has been set\033[0m")

    # Initialise counters
    tagged = 0
    iteration = 0

    # Get all files in paths
    files = []
    for arg in parser.path:
        p = Path(arg)
        if p.is_dir():
            files.extend((f, p) for f in p.glob('**/*') if f.is_file())
        elif p.is_file():
            files.append((p, p.parent))
        else:
            invalid.append(arg)

    # Iterate through files and add lyric tags
    for file_path in files:
        if not parser.no_bar:
            iteration += 1
            print_progress(iteration, len(files), prefix="Nomming...", bar_length=50)

        try:
            if parser.force != None:
                tag.delete_lyrics(file_path[0], parser.force)
            tag.add_lyrics(file_path[0])

        except UnknownTypeError:
            # Ignore unrecognised files
            log.debug("Unknown file type: %s", file_path[0].relative_to(file_path[1]))

        except UnsupportedTypeError as e:
            unsupported.append((file_path[0].relative_to(file_path[1]), e))

        except LyricsNotFoundError:
            log.debug("Lyrics not found: %s", file_path[0].relative_to(file_path[1]))
            notfound.append(file_path[0].relative_to(file_path[1]))

        except ExistingLyricsError:
            log.debug("Existing lyrics: %s", file_path[0].relative_to(file_path[1]))
            existing.append(file_path[0].relative_to(file_path[1]))

        except ConnectionError as e:
            log.debug("Connection error: couldn't connect to any sources")
            sys.exit("nom.py: error: please check your internet connection")

        else:
            log.debug("Lyrics added: %s", file_path[0].relative_to(file_path[1]))
            tagged += 1

    # Print output to user
    print_results(tagged)


def parse_args(args):
    """Parse user input"""
    parser = argparse.ArgumentParser(
            description="""Command line tool to add lyrics to music files.
                        Relies on track title and artist tags to find lyrics.
                        Supported file types: {}.""".format(", ".join(supported_types)))
    parser.add_argument('path', metavar='PATH', nargs='+', 
                        help='path of file or directory to be tagged')
    parser.add_argument('-f', '--force', metavar='STRING', nargs='*', 
                        help="""overwrite lyrics containing STRING (case insensitive), 
                                or all lyrics if no STRING given""")
    parser.add_argument('-v', '--verbose', action='store_true', 
                        help='list the files that failed')
    parser.add_argument('--no-bar', action='store_true', 
                        help='don\'t show the progress bar')
    parser.add_argument('--debug', action='store_true', help=argparse.SUPPRESS)

    return parser.parse_args(args)


def log_setup(parser):
    """Set up logger to print to user"""
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


# https://gist.github.com/aubricus/f91fb55dc6ba5557fbab06119420dd6a
def print_progress(iteration, total, prefix='', suffix='', decimals=1, bar_length=100):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        bar_length  - Optional  : character length of bar (Int)
    """
    str_format = "{0:." + str(decimals) + "f}"
    percents = str_format.format(100 * (iteration / float(total)))
    filled_length = int(round(bar_length * iteration / float(total)))
    bar = '█' * filled_length + '-' * (bar_length - filled_length)

    sys.stdout.write('\r%s |%s| %s%s %s' % (prefix, bar, percents, '%', suffix)),

    if iteration == total:
        sys.stdout.write('\n\n')
    sys.stdout.flush()


def print_results(tagged):
    """Print output to console for user"""
    log.debug('-' * 60)

    # Print number of files tagged
    if tagged:
        log.warning("\033[32mSuccessfully added lyrics to %d files\033[0m", tagged)

    # Print error for lyrics not found
    if notfound:
        log.info('\033[33m')
        log.warning("Lyrics not found for %d files\033[0m", len(notfound))
        for f in notfound:
            log.info(f)

    # Print error for existing lyrics on file
    if existing:
        log.info('\033[33m')
        log.warning("Existing lyrics on %d files\033[0m", len(existing))
        for f in existing:
            log.info(f)

    # Print error for unsupported file type
    if unsupported:
        log.info('\033[33m')
        log.warning("Unsupported file type for %d files\033[0m", len(unsupported))
        for f in unsupported:
            log.info(str(f[0]) + " ('" + str(f[1]) + "')")

    # Print invalid paths
    if invalid:
        log.info('\033[31m')
        for i in invalid:
            log.warning("Invalid path '%s'", i)
        log.info('\033[0m')