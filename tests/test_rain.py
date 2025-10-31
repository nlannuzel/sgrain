import unittest
import requests_mock
from nlannuzel.sgrain.rain import RainAreas
from nlannuzel.sgrain.geo import Location
from nlannuzel.sgrain.graph import Pixel, Color
import datetime

def mock_load_image(rain, year, month, day, hour, minute):
    # dpsri_70km_2025101516e300000dBR.dpsri.png
    # image from 2025/10/15 16:30
    png_image = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\xd9\x00\x00\x00x\x08\x06\x00\x00\x00\x7f\xfeW=\x00\x00\x03oIDATx\xda\xed\xdd1n\x13A\x14\x06`wT\x14\x1c#\x07@B\xa2B\x08\xc4y\xe8\x91\x90\xa8\xc8\x05\x90(\x91\xb8\x00M$\x1a:\n\xba\x144(w\x08\r\xf5\xb2\xffz\x9f\xbd@\x12\xe2x\'v\x92\xef\xb3Fk\xc7\xa41\xf9\xfdffgv\x17\x0b\xd8\x85\xe3\xef\x9d\x0f\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xe0\x86z\xf7\xde\xbd\xa8`\xafCvz\xba\xd9\xefw\x9dPC\xd3\x90\x01\xc0\xfe\xd1\x05\x04\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xae\x87=y\xd0\x98K@\x00\x00\x00l\xc6%\x17\xa0\xa1\xcc\x06\x1e\x7f\xef\x04\xcd\x97\x16-}\xfe\xd2\r\xcd\xf4;\xcc(\xd5\xab*X\x02\x96\xa9\xf77\xaf\x96?\x03\xb6\xacZ\t\xd4\xb7\x07\xcbV\xc1\xca\xf1\xf5\xb3\xe51\xfff\xda\x9d\x046\xac`\t\xd7\x87\x87\xeb\x90U5K\xc8\x8e\x0e\x96\xef\xe5\x08\xcc4H\xaf\xaebBV\xe1K\xfbuo\x19\xb6ie\x03\xae \x01{\xfbh]\xc1\xd2*diy\x9e\xf7u\x1d\xe1\x8a*`iy\x9e\x96\xa0\xd51A\xfbq\xbf\xb3.\x11\xae\xda]\xac\x80U\x05\xab\x80U\x17Rw\x11\xb6\x08X\xdat"\xa4\x02\x97`9I\r\x17\x84\xe7\xb2j\x9cU\x93\x1fy-X\x00\xdc\xadj\x88?\x06`[\x19Gd\xd0\x0e4\xa8X5\x1b&d\xb0e\xa5\xaaY\xb0\x1ckkF-\t\xaa\x95\t\xc0\x16\x01\xabuuYy\xd0?\x9evO\xd6\xab\xc6\x8f\x0e\xba\x17\xdd\xf3\xa1Y\x95`\x0c\xcc\xa6rB\xb4V\x88\xf7\xd5*A\x1aO\xa1.\x03Wk\xed\xfa\xf7\xba\xee\xf1\xb2\xa2\xe5w\xea\x84\xaa\xf5v\xf0\x9f*V]\xc3\x84\xa6\x7f\x0c!\xfb\xd4\x87\xec\xebb8\x0e\x15-a\xeb\xc3\x95\xe7\xab\xd7\xb5\x8d\xe3\xac\x90\t\x1e\xfc\x15\xb2\xac\xa3\xeb\x83\xb3\xaab\x87\x93\xf6r1T\xb0\xbc\x97\x80\xe5\xf9P\xe5\xf2\xa8\xa0\x01\xe7\xa8*\x96\xee\xe0\xd8E\xecN&\xe1\xca\xf1\xe3\xf8\xb3\xb1\xca\xad\xc6k\xf5H7\xd38\x02\xceQ\xeb\xe9R\xc92\xe6\xfa9\x86\xeap\x0c\xd6\xc9\xba\xdbX!\x1b\x026\x8e\xdd\x86J\x96\x90\x01\x17Lz$h\xb5\xdfi\x9c\xaa\xef\xc6j\xb5\nU\x1e\x15\xac\xda\xf7\x94p\xa6\x99m\x9c\x8f\x1e\xc1-\xaefi\x93)\xfc\xd5t\xfdtF\xb1\xa6\xf7\xcd*\xb6\x1b\x1f\xfb\xc2\xba\xc5\xdf\x9eu\x01\xce\xfc\'\xf7!\x1a\x82\x95G\xc6j\xe3\xcc\xe2j\x93a^\xeb"\xc2\x06\xdf\x9e\x15\xb4\xb4\x84\xa7o5\xee\x1aZ]\xe2\xac\xae#X\x977s\xfd@\xd8"tc\x97\xf1\x8fq\x82\xf1B\xfb\xcf^\x17\xfc\x8eH\x17\xf1\xbcs_\xfe\x08\xa0AU\xe3\xfa\xc6\xc6\x00\x00\x00\x00\x00\xb0C\xa6\xaa\xa11\xe7\xdf\x00\xa0\xd4"e]P\x8c\xb3\x1a\xa9\xdd\x01B\xc6\xde\xc9\xde\xb0\xdb\x12\xec\x04M\xc8\xd8;\xd3U\xf6-\xf6\x85\xb5\xfe\xa3\xaf\x8d\xa6\xb0\xf7\xd5\xac\xd5\xc6\xcb\xdai\r\xaaY\x83JV\x9b\x0fU\x1a\x00\x80\x1ba\xdbn\xdb\xf4b;\xc0\x19r\xb5\xa9]\x07\x15\xb8$\xd5\xccg\n7\xae+_\xf7\x87\xab+9\xcf\xd1\xf3\xe0\x8e\x8f\xf1\xf87d\xd3\x80\xf9|\x11\xb4\x99\xc7\xcbu\x97\xd3\x9c\xb7\x142h0\x1eK\xa8V7\x106>cW\xdf\xf6@#u\xdf4\xdf\xf0\xd08h\xc6)\xd0\xc0\xf4\x1ehn\xfe\x0e3K\xa8j\xc6\r\x98Q\xba\x855\xad==\x7f\x04\xcc\x1c\xb4\xba\x7f\xb2;zBc\xaa\x18\x00\xc0L~\x03>\xe7\x90\n\xb3\xf2\xfe\xcd\x00\x00\x00\x00IEND\xaeB`\x82'
    dt = datetime.datetime(year, month, day, hour, minute)
    filename = f"dpsri_70km_{year}{month:02d}{day:02d}{hour:02d}{minute:02d}0000dBR.dpsri.png"
    url = f"https://www.weather.gov.sg/files/rainarea/50km/v2/{filename}"
    with requests_mock.Mocker() as m:
        m.get(url, content = png_image)
        rain.load_image(dt)

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
        mock_load_image(rain, 2025, 10, 15, 16, 30)
        location1 = Location(1.313383, 103.815203)
        pixel = rain.location_to_pixel(location1)
        location2 = rain.pixel_to_location(pixel)
        self.assertAlmostEqual(location1.lon, location2.lon, 3)
        self.assertAlmostEqual(location1.lat, location2.lat, 3)

    def test_intensity_at(self):
        rain = RainAreas()
        mock_load_image(rain, 2025, 10, 15, 16, 30)
        p = Pixel(91, 66)
        location = rain.pixel_to_location(p)
        rain.intensity_map.set_color_at(p.i, p.j, Color.grey(1))
        self.assertEqual(rain.intensity_at(location), 1)
        self.assertAlmostEqual(rain.intensity_at(location, 1), 1/9)
        self.assertAlmostEqual(rain.intensity_at(location, 2), 1/25)

    def test_noise(self):
        rain = RainAreas()
        mock_load_image(rain, 2025, 10, 15, 16, 30)

        def count_blobs_of_size(n):
            count = 0
            for blob in rain.filter_blobs(lambda blob:len(blob)==n):
                count += 1
            return count

        initial_blobs_count = 40
        noise_count = 23
        self.assertEqual(len(rain.blobs), initial_blobs_count)
        self.assertEqual(count_blobs_of_size( 186 ),  1          )
        self.assertEqual(count_blobs_of_size(  92 ),  1          )
        self.assertEqual(count_blobs_of_size(  24 ),  1          )
        self.assertEqual(count_blobs_of_size(  16 ),  1          )
        self.assertEqual(count_blobs_of_size(   7 ),  2          )
        self.assertEqual(count_blobs_of_size(   6 ),  1          )
        self.assertEqual(count_blobs_of_size(   3 ),  3          )
        self.assertEqual(count_blobs_of_size(   2 ),  7          )
        self.assertEqual(count_blobs_of_size(   1 ), noise_count )  # noise

        rain.remove_noise()
        self.assertEqual(len(rain.blobs), initial_blobs_count - noise_count)
        self.assertEqual(count_blobs_of_size( 186 ), 1 )
        self.assertEqual(count_blobs_of_size(  92 ), 1 )
        self.assertEqual(count_blobs_of_size(  24 ), 1 )
        self.assertEqual(count_blobs_of_size(  16 ), 1 )
        self.assertEqual(count_blobs_of_size(   7 ), 2 )
        self.assertEqual(count_blobs_of_size(   6 ), 1 )
        self.assertEqual(count_blobs_of_size(   3 ), 3 )
        self.assertEqual(count_blobs_of_size(   2 ), 7 )
        self.assertEqual(count_blobs_of_size(   1 ), 0 )  # gone!

if __name__ == '__main__':
    unittest.main()
