import unittest

from app.core.palette import classify_season
from app.core.palettes_colors import SEASON_PALETTES


def make_color(lightness, a, b, luminosity, chromaticity):
    return {
        "lab": (lightness, a, b),
        "luminosity_category": luminosity,
        "chromaticity_category": chromaticity,
    }


class ClassifySeasonTests(unittest.TestCase):
    def test_each_season_selects_its_palette(self):
        cases = [
            # Piel cálida, clara y brillante -> Primavera
            (
                make_color(70, 0, 1, "light", "intense"),
                make_color(50, 0, 0, "dark", "soft"),
                make_color(40, 0, 0, "dark", "soft"),
                "Primavera",
            ),
            # Piel cálida, no clara -> Otoño
            (
                make_color(60, 0, 1, "medium", "soft"),
                make_color(59, 0, 0, "medium", "soft"),
                make_color(58, 0, 0, "medium", "soft"),
                "Otoño",
            ),
            # Piel fría, clara, suave y bajo contraste -> Verano
            (
                make_color(70, 1, 0, "light", "soft"),
                make_color(69, 0, 0, "light", "soft"),
                make_color(68, 0, 0, "light", "soft"),
                "Verano",
            ),
            # Piel fría con alto contraste -> Invierno
            (
                make_color(70, 1, 0, "light", "soft"),
                make_color(40, 0, 0, "dark", "soft"),
                make_color(30, 0, 0, "dark", "soft"),
                "Invierno",
            ),
        ]

        for skin, eyes, hair, expected_season in cases:
            with self.subTest(expected_season=expected_season):
                season = classify_season(skin, eyes, hair)
                self.assertEqual(season, expected_season)

                palette = SEASON_PALETTES[season]
                self.assertEqual(len(palette), 8)
                self.assertTrue(all(color.startswith("#") for color in palette))


if __name__ == "__main__":
    unittest.main()