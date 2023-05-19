from unittest import TestCase
from tunepalapi import Song
from datetime import date


class TestSong(TestCase):
    year_now = date.today().year

    def test_constructor(self):

        song_titles = ['here', '24www', 'text', 55, 'rec', 'terw', 'aaa']
        song_artists = ['dimmu', 'pantera', 'slayer', 74, 'tek', 'qwe', 'qwerw']
        song_release_years = [1992, 2002, 1800, 1000, '', '1999', self.year_now]
        for x in range(len(song_titles)):
            self.song = Song(song_titles[x], song_artists[x], song_release_years[x])
            self.assertEqual(song_titles[x], self.song.title)
            self.assertEqual(song_artists[x], self.song.artist)
            self.assertEqual(str(song_release_years[x]), self.song.release_year)

        song_titles_for_exception = ['roadway', '', 'building', 'qq77', '123', '', 'test']
        song_artists_for_exception = ['34rty', '', 'rocking', 'ontheway', 'num91', '', 'one']
        song_release_years_for_exception = [23456, '', -2000, self.year_now + 1, 999, 1999, 1.123]
        for x in range(len(song_artists_for_exception)):
            self.assertRaises(ValueError, Song, song_titles_for_exception[x], song_artists_for_exception[x],
                              song_release_years_for_exception[x])

        # Replace invalid release year with ''
        self.song = Song('qweqwe12q', 'asa', 'test.com')
        self.assertEqual('', self.song.release_year)

        self.song = Song('qwe', 'we12w3qweqa', '10')
        self.assertEqual('', self.song.release_year)
