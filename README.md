# LyricNommer
Nom lyrics from the Internet. Supports *MP3*, *FLAC*, *Ogg*, and *AIFF* formats.

## Installation
Download the souce code from the [latest release](https://github.com/mtsev/lyricnommer/releases/latest).

LyricNommer requires Python 3 to run. Dependencies can be installed using pip.
```bash
pip install -r requirements.txt
```

## Usage
Given one or more paths to files and/or directories, LyricNommer will search online 
for lyrics for all the files, including in subdirectories. If it finds any, 
it will add them to the file as lyrics metadata.
```bash
./nom.py "~/Desktop/my song.mp3" ~/Music
```

By default, LyricNommer will not add lyrics to files that already have them.
You can force LyricNommer to overwrite existing lyrics using the `-f` option.
```bash
./nom.py -f ~/Music
```

You can also only overwrite files which contain certain lyrics.
```bash
./nom.py -f badword "bad phrase" ~/Music    # overwrite lyrics containing "badword" or "bad phrase"
```

You can see all available options using the `-h` option.
```bash
./nom.py -h
```

## Sources
LyricNommer looks for lyrics on these websites:
* metrolyrics.com
* lyrics.wikia.com
* genius.com
