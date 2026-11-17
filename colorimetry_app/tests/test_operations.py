import unittest

from PIL import Image

from app.core.operations import get_representative_color


class RepresentativeColorTests(unittest.TestCase):
    def test_edge_region_is_clipped_to_image_bounds(self):
        image = Image.new("RGB", (3, 2))
        image.putdata([
            (10, 20, 30),
            (20, 30, 40),
            (30, 40, 50),
            (40, 50, 60),
            (50, 60, 70),
            (60, 70, 80),
        ])

        self.assertEqual(get_representative_color(image, 0, 0), (35, 45, 55))

    def test_grayscale_image_returns_rgb_channels(self):
        image = Image.new("L", (3, 3), 73)

        self.assertEqual(get_representative_color(image, 1, 1), (73, 73, 73))


if __name__ == "__main__":
    unittest.main()
