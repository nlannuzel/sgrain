import unittest
from nlannuzel.sgrain.rain import RainAreas
from nlannuzel.sgrain.geo import Location
from nlannuzel.sgrain.graph import Image, Pixel, Color
import datetime

class TestRain(unittest.TestCase):
    def test_round(self):
        rain = RainAreas()

        self.assertEqual(len(rain.color_scale), 32)

        sx = 217 / (rain.bottom_right.lon - rain.top_left.lon)
        sy = 120 / (rain.top_left.lat - rain.bottom_right.lat)
        error = abs(1 - sx/sy)
        self.assertTrue( error < 2/100 )

        rounded = rain.round_to_previous_5_min(datetime.datetime(year = 2025, month = 10, day = 11, hour = 12, minute = 13))
        self.assertEqual( rounded.year  , 2025)
        self.assertEqual( rounded.month , 10)
        self.assertEqual( rounded.day   , 11)
        self.assertEqual( rounded.hour  , 12)
        self.assertEqual( rounded.minute, 10)

        rounded = rain.round_to_previous_5_min(datetime.datetime(year = 2025, month = 10, day = 11, hour = 12, minute = 20))
        self.assertEqual( rounded.year  , 2025)
        self.assertEqual( rounded.month , 10)
        self.assertEqual( rounded.day   , 11)
        self.assertEqual( rounded.hour  , 12)
        self.assertEqual( rounded.minute, 20)

    def test_location_to_pixel(self):
        rain = RainAreas()
        rain.intensity_map = Image(217, 120)
        location1 = Location(1.313383, 103.815203)
        pixel = rain.location_to_pixel(location1)
        location2 = rain.pixel_to_location(pixel)
        self.assertAlmostEqual(location1.lon, location2.lon, 3)
        self.assertAlmostEqual(location1.lat, location2.lat, 3)

    def test_intensity_at(self):
        rain = RainAreas()
        rain.intensity_map = Image(217, 120)
        location = Location(1.313383, 103.815203)
        p = rain.location_to_pixel(location)
        rain.intensity_map.set_color_at(p.i, p.j, Color.grey(1))
        self.assertEqual(rain.intensity_at(location), 1)
        self.assertAlmostEqual(rain.intensity_at(location, 1), 1/9)
        self.assertAlmostEqual(rain.intensity_at(location, 2), 1/25)

    def test_noise(self):
        rain = RainAreas()
        rain.intensity_map = Image(rows = [[Color.grey(v) for v in row] for row in [
            [ 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ],
            [ 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0 ],
            [ 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0 ],
            [ 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0 ],
            [ 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 1, 1, 0 ],
            [ 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0 ],
            [ 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0 ],
            [ 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0 ],
            [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1 ],
            ]])

        def count_blobs_of_size(n):
            count = 0
            for blob in rain.filter_blobs(lambda blob:len(blob)==n):
                count += 1
            return count

        self.assertEqual(len(rain.blobs), 8)
        self.assertEqual(count_blobs_of_size(25), 1)
        self.assertEqual(count_blobs_of_size(18), 1)
        self.assertEqual(count_blobs_of_size(6), 2)
        self.assertEqual(count_blobs_of_size(2), 2)
        self.assertEqual(count_blobs_of_size(1), 2)

        rain.original_image = rain.intensity_map
        rain.remove_noise()
        self.assertEqual(len(rain.blobs), 6)
        self.assertEqual(count_blobs_of_size(25), 1)
        self.assertEqual(count_blobs_of_size(18), 1)
        self.assertEqual(count_blobs_of_size(6), 2)
        self.assertEqual(count_blobs_of_size(2), 2)
        self.assertEqual(count_blobs_of_size(1), 0)

if __name__ == '__main__':
    unittest.main()
