from typing import List
from datetime import date
import csv


class Song:
    title: str = ''
    artist: str = ''
    release_year: str = ''

    def __init__(self, title, artist, release_year):
        if release_year == '' and title != '' and artist != '':
            self.title = title
            self.artist = artist
            self.release_year = release_year
        elif isinstance(release_year, int) and title != '' and artist != ''\
                and 1000 <= release_year <= date.today().year:
            self.title = title
            self.artist = artist
            self.release_year = str(release_year)
        elif isinstance(release_year, str) and title != '' and artist != '':
            try:
                release_year = int(release_year)
                if 1000 <= release_year <= date.today().year:
                    self.title = title
                    self.artist = artist
                    self.release_year = str(release_year)
                else:
                    raise ValueError("Year value out of range")
            except ValueError:
                self.title = title
                self.artist = artist
                self.release_year = ''
        else:
            raise ValueError("Incorrect Value")


class TunePalAPI:

    songs: List[Song] = []  # holds all songs available from this API
    page_size: int  # allows the user to decide how many songs are returned per page
    current_page_index: int
    amount_of_pages: int

    def __init__(self, page_size=None):

        if page_size <= 0 or page_size > 50 or type(page_size) == str or type(page_size) == float:
            raise ValueError("Invalid page value")
        else:
            self.songs = []
            self.page_size = page_size
            self.current_page_index = 0
            with open('songlist.csv') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    title = row['Song Clean']
                    artist = row['ARTIST CLEAN']
                    release_year = row['Release Year']
                    self.songs.append(Song(title, artist, release_year))
                self._set_amount_of_pages(self.page_size)

    """Takes a list of songs and returns a smaller window using the 
    current_page_index and page_size"""
    def _build_song_window(self, song_list: List[Song]):
        first_index = self.current_page_index * self.page_size
        last_index = first_index + self.page_size
        return song_list[first_index:last_index]

    """Adds a song, but only if it isn't already in the list"""
    def add_song(self, title: str, artist: str, release_year: str):
        try:
            release_year = int(release_year)
            if release_year < 1000 or release_year > date.today().year:
                raise ValueError("Out of date range")
            else:
                release_year = str(release_year)
        except ValueError:
            raise ValueError("invalid year")
        same_song_found = False
        for song in self.songs:
            if song.title.lower() == title.lower() and song.artist.lower() == artist.lower():
                same_song_found = True
                break
        if same_song_found:
            return False
        else:
            self.songs.append(Song(title, artist, release_year))
            return True

    """Return a page of songs, use next_page and previous_page to change the window"""
    def get_songs(self):
        return self._build_song_window(self.songs)

    """Tells the API to move to the previous page"""
    def next_page(self):
        if self.current_page_index < self.amount_of_pages:
            self.current_page_index = self.current_page_index + 1
        else:
            self.current_page_index = self.amount_of_pages

    """Tells the API to move to the next page"""
    def previous_page(self):
        if self.current_page_index > 0:
            self.current_page_index = self.current_page_index - 1
        else:
            self.current_page_index = 0

    """Set amount of pages based on song list length and page size"""

    def _set_amount_of_pages(self, page_size=int):
        if isinstance(page_size, float):
            raise TypeError("Only integer type accepted")
        remainder = len(self.songs) % page_size
        if remainder > 0:
            zero_modulus_result = len(self.songs) - remainder
            self.amount_of_pages = (zero_modulus_result / page_size) + 1
        else:
            self.amount_of_pages = len(self.songs) / page_size

    """Set the page_size parameter, controlling how many songs are returned"""
    def set_page_size(self, page_size: int):
        if isinstance(page_size, float):
            raise TypeError("Only integer type accepted")

        if page_size <= 0 or page_size > 50:
            raise ValueError("Page size should be between 1 or 50")
        self.page_size = page_size
        self._set_amount_of_pages(page_size)

    """The search() function matches any songs whose title or artist starts
        with the query provided. E.G. a query of "The" would match "The Killers"
        "The Libertines" etc.
    """
    def search(self, starts_with_query: str):
        hits = []
        for song in self.songs:
            if song.title.lower().startswith(starts_with_query.lower()) or \
                    song.artist.lower().startswith(starts_with_query.lower()):
                hits.append(song)
        return self._build_song_window(hits)

    """Allows users to filter out old-person music. Filter songs to only return
        songs released since a certain date. e.g. a query of 2022 would only return
        songs released this year 
    """
    def get_songs_since(self, release_year: int):
        if isinstance(release_year, float):
            raise TypeError("Invalid year format")
        elif release_year > date.today().year:
            raise ValueError("Year out of range")
        hits = []
        for song in self.songs:
            if song.release_year != '' and int(song.release_year) >= release_year:
                hits.append(song)
        return self._build_song_window(hits)
