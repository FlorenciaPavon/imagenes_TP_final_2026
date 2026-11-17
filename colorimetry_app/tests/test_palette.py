import unittest
import math

from app.core.palette import (
    classify_chromaticity,
    classify_luminosity,
    classify_season,
)
from app.core.palettes_colors import SEASON_PALETTES


def make_color(lightness, a, b):
    return {
        "lab": (lightness, a, b),
        "chromaticity": math.sqrt(a**2 + b**2),
    }


class ClassifySeasonTests(unittest.TestCase):
    def test_each_season_selects_its_palette(self):
        cases = [
            # Piel cálida, clara y brillante -> Primavera
            (
                make_color(70, 0, 25),
                make_color(50, 0, 0),
                make_color(40, 0, 0),
                "Primavera",
                "high",
            ),
            # Piel cálida, oscura y suave -> Otoño
            (
                make_color(60, 0, 5),
                make_color(59, 0, 0),
                make_color(58, 0, 0),
                "Otoño",
                "high",
            ),
            # La luminosidad media no debe dejar sin estación un caso cálido.
            (
                make_color(62, 20, 24),
                make_color(60, 0, 0),
                make_color(58, 0, 0),
                "Otoño",
                "medium",
            ),
            # Piel fría, clara y suave -> Verano; alto contraste reduce la confianza
            (
                make_color(81.57, 7, 3),
                make_color(51.37, -2, -22),
                make_color(58.04, 5, -1),
                "Verano",
                "medium",
            ),
            # Piel fría, oscura e intensa -> Invierno
            (
                make_color(50, 25, -5),
                make_color(30, 0, 0),
                make_color(20, 0, 0),
                "Invierno",
                "high",
            ),
        ]

        for skin, eyes, hair, expected_season, expected_confidence in cases:
            with self.subTest(expected_season=expected_season):
                result = classify_season(skin, eyes, hair)
                season = result["season"]
                self.assertEqual(season, expected_season)
                self.assertEqual(result["confidence"], expected_confidence)

                palette = SEASON_PALETTES[season]
                self.assertEqual(len(palette), 8)
                self.assertTrue(all(color.startswith("#") for color in palette))

    def test_undetermined_temperature_returns_no_season_and_low_confidence(self):
        skin = make_color(70, 5, 5)
        eyes = make_color(50, 0, 0)
        hair = make_color(40, 0, 0)

        result = classify_season(skin, eyes, hair)

        self.assertEqual(result["temperature"], "undetermined")
        self.assertEqual(result["season"], "No determinada")
        self.assertEqual(result["confidence"], "low")

    def test_small_negative_temperature_delta_uses_sign_with_low_confidence(self):
        skin = make_color(7.45, 1, -1)
        eyes = make_color(21.18, 11, 10)
        hair = make_color(9.80, 2, -1)

        result = classify_season(skin, eyes, hair)

        self.assertEqual(result["temperature_delta"], -2)
        self.assertEqual(result["temperature"], "cool")
        self.assertEqual(result["luminosity"], "dark")
        self.assertEqual(result["chromaticity"], "soft")
        self.assertEqual(result["season"], "Invierno")
        self.assertEqual(result["confidence"], "low")

    def test_small_positive_temperature_delta_uses_sign_with_low_confidence(self):
        skin = make_color(62, 10, 12)
        eyes = make_color(60, 0, 0)
        hair = make_color(58, 0, 0)

        result = classify_season(skin, eyes, hair)

        self.assertEqual(result["temperature_delta"], 2)
        self.assertEqual(result["temperature"], "warm")
        self.assertEqual(result["season"], "Otoño")
        self.assertEqual(result["confidence"], "low")


class ColorCategoryBoundaryTests(unittest.TestCase):
    def test_luminosity_threshold_boundaries(self):
        self.assertEqual(classify_luminosity(60.33), "dark")
        self.assertEqual(classify_luminosity(60.34), "medium")
        self.assertEqual(classify_luminosity(64.32), "medium")
        self.assertEqual(classify_luminosity(64.33), "light")

    def test_chromaticity_threshold_boundaries(self):
        self.assertEqual(classify_chromaticity(20.04), "soft")
        self.assertEqual(classify_chromaticity(20.05), "medium")
        self.assertEqual(classify_chromaticity(22.05), "medium")
        self.assertEqual(classify_chromaticity(22.06), "intense")
if __name__ == "__main__":
    unittest.main()