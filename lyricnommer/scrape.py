import scrapers.metrolyrics as metrolyrics

# Get lyrics from metrolyrics.com
def scrape_metrolyrics(title, artist):
    if not (title and artist):
        print("No?")
        return ""

    parser = metrolyrics.Parser(artist, title)
    try:
        lyrics = parser.parse()
    except Exception as e:
        print("Error in metrolyrics parser")
        print(str(e))
        return ""

    return lyrics



