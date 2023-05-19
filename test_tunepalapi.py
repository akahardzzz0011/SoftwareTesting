from unittest import TestCase
from tunepalapi import TunePalAPI
from datetime import date


class TestTunePalAPI(TestCase):
    year_now = date.today().year

    def setUp(self) -> None:
        self.set_up_tunepalapi = TunePalAPI(50)

    def test_constructor(self):
        page_values = [5, 1, 50]
        for x in range(len(page_values)):
            self.tunepal = TunePalAPI(page_values[x])
            self.assertEqual(page_values[x], self.tunepal.page_size)

        invalid_page_values = [-9, 55, 0, 51, 1.21]
        invalid_page_types = ['qwe', '', None]
        for x in range(len(invalid_page_values)):
            self.assertRaises(ValueError, TunePalAPI, invalid_page_values[x])

        for x in range(len(invalid_page_types)):
            self.assertRaises(TypeError, TunePalAPI, invalid_page_types[x])

    def test_build_song_window(self):
        page_size = [3, 5, 4, 10]
        for x in range(len(page_size)):
            self.tunepal = TunePalAPI(page_size[x])
            self.assertEqual(page_size[x], len(self.tunepal._build_song_window(self.tunepal.songs)))

        song_list_result = self.set_up_tunepalapi._build_song_window(self.set_up_tunepalapi.songs)
        for x in range(len(song_list_result)):
            self.assertEqual(song_list_result[x].title, self.set_up_tunepalapi.songs[x].title)
            self.assertEqual(song_list_result[x].artist, self.set_up_tunepalapi.songs[x].artist)
            self.assertEqual(song_list_result[x].release_year, self.set_up_tunepalapi.songs[x].release_year)

    def test_add_song(self):
        song_release_years_for_exception = [23456, '', -2000, self.year_now + 1, 999, 1.123, 'stringyear']

        for x in range(len(song_release_years_for_exception)):
            self.assertRaises(ValueError, self.set_up_tunepalapi.add_song, 'test', 'tested',
                              song_release_years_for_exception[x])

        # Song not added
        i = int(0)
        for x in range(len(self.set_up_tunepalapi.songs)):
            self.assertFalse(self.set_up_tunepalapi.add_song(
                artist=self.set_up_tunepalapi.songs[x].artist,
                title=self.set_up_tunepalapi.songs[x].title,
                release_year='1999'
            ))
        self.assertFalse(self.set_up_tunepalapi.add_song(
            artist='.38 Special', title='Caught Up in You', release_year='1991'
        ))
        # Song added
        self.assertTrue(self.set_up_tunepalapi.add_song(
            artist='is not', title='in the list', release_year=1888
        ))
        self.assertEqual('is not', self.set_up_tunepalapi.songs[-1].artist)
        self.assertEqual('in the list', self.set_up_tunepalapi.songs[-1].title)
        self.assertEqual('1888', self.set_up_tunepalapi.songs[-1].release_year)

    def test_get_songs(self):
        results = self.set_up_tunepalapi.get_songs()
        for x in range(len(results)):
            self.assertEqual(self.set_up_tunepalapi.songs[x].title, results[x].title)
            self.assertEqual(self.set_up_tunepalapi.songs[x].artist, results[x].artist)
            self.assertEqual(self.set_up_tunepalapi.songs[x].release_year, results[x].release_year)

    def test_next_page(self):
        self.assertEqual(0, self.set_up_tunepalapi.current_page_index)
        for x in range(1, 10):
            self.set_up_tunepalapi.next_page()
            self.assertEqual(x, self.set_up_tunepalapi.current_page_index)

        self.set_up_tunepalapi.current_page_index = 50
        self.set_up_tunepalapi.amount_of_pages = 50
        for x in range(5):
            self.set_up_tunepalapi.next_page()
            self.assertEqual(50, self.set_up_tunepalapi.current_page_index)

        self.set_up_tunepalapi.current_page_index = 57
        self.set_up_tunepalapi.amount_of_pages = 56
        for x in range(5):
            self.set_up_tunepalapi.next_page()
            self.assertEqual(56, self.set_up_tunepalapi.current_page_index)

    def test_previous_page(self):
        self.set_up_tunepalapi.previous_page()
        self.assertEqual(0, self.set_up_tunepalapi.current_page_index)

        self.set_up_tunepalapi.current_page_index = 11
        for x in range(10, 0, -1):
            self.set_up_tunepalapi.previous_page()
            self.assertEqual(x, self.set_up_tunepalapi.current_page_index)

        self.set_up_tunepalapi.current_page_index = 0
        for x in range(5):
            self.set_up_tunepalapi.previous_page()
            self.assertEqual(0, self.set_up_tunepalapi.current_page_index)

    def test_set_amount_of_pages(self):
        invalid_types = ['qwe', None, 14.4]
        for x in range(len(invalid_types)):
            self.assertRaises(TypeError, self.set_up_tunepalapi._set_amount_of_pages, invalid_types[x])
        self.set_up_tunepalapi._set_amount_of_pages(3)
        self.assertEqual(743, self.set_up_tunepalapi.amount_of_pages)

    def test_set_page_size(self):
        invalid_type = ['qwe', None, 12.3]
        invalid_value = [51, 0]
        accepted_values = [1, 5, 12, 27, 50]
        for x in range(len(invalid_type)):
            self.assertRaises(TypeError, self.set_up_tunepalapi.set_page_size, invalid_type[x])
        for y in range(len(invalid_value)):
            self.assertRaises(ValueError, self.set_up_tunepalapi.set_page_size, invalid_value[y])
        for z in range(len(accepted_values)):
            self.set_up_tunepalapi.set_page_size(accepted_values[z])

    def test_search(self):
        searches = ['the', 'The', '.38']
        for x in range(len(searches)):
            self.assertTrue(self.set_up_tunepalapi.search(searches[x]))

        results = self.set_up_tunepalapi.search('Door')
        self.assertFalse(results)

    def test_get_songs_since(self):
        invalid_values = [2222, 2024, 3000]
        invalid_types = ['2223', '2000', '1999', 'year', 222.2]
        accepted_values = [2000, 1999, 1995, 1200]
        for x in range(len(invalid_values)):
            self.assertRaises(ValueError, self.set_up_tunepalapi.get_songs_since, invalid_values[x])
        for y in range(len(invalid_types)):
            self.assertRaises(TypeError, self.set_up_tunepalapi.get_songs_since, invalid_types[y])
        for z in range(len(accepted_values)):
            self.assertTrue(self.set_up_tunepalapi.get_songs_since(accepted_values[z]))
