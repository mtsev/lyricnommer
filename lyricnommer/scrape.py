import scrapers.metrolyrics as metrolyrics
import scrapers.darklyrics as darklyrics

# Get lyrics from metrolyrics.com
def scrape_metrolyrics(title, artist):
    if not (title and artist):
        return ""

    parser = metrolyrics.Parser(artist, title)
    try:
        lyrics = parser.parse()
    except Exception as e:
        print("Error in metrolyrics parser")
        print(str(e))
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
        print("Error in darklyrics parser")
        print(str(e))
        return ""

    return lyrics



