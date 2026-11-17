import io
import json
import unittest

import httpx
from PIL import Image

from app.config import MAX_SIZE_BYTES
from app.main import app


class AnalyzeEndpointTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        transport = httpx.ASGITransport(app=app)
        self.client = httpx.AsyncClient(
            transport=transport,
            base_url="http://testserver",
        )

    async def asyncTearDown(self):
        await self.client.aclose()

    @staticmethod
    def make_png(width=2, height=2):
        image_bytes = io.BytesIO()
        Image.new("RGB", (width, height), (120, 80, 40)).save(image_bytes, format="PNG")
        return image_bytes.getvalue()

    @staticmethod
    def valid_selections():
        return {
            "skin": {"x": 0, "y": 0},
            "eyes": {"x": 1, "y": 1},
            "hair": {"x": 1, "y": 0},
        }

    async def post_analysis(self, image, selections):
        return await self.client.post(
            "/api/analyze",
            files={"file": ("sample.png", image, "image/png")},
            data={"selections_json": selections},
        )

    def assert_domain_error(self, response, status_code, error_code):
        self.assertEqual(response.status_code, status_code)
        detail = response.json()["detail"]
        self.assertEqual(detail["code"], error_code)
        self.assertTrue(detail["message"])

    async def test_file_over_limit_returns_413(self):
        response = await self.post_analysis(
            b"x" * (MAX_SIZE_BYTES + 1),
            json.dumps(self.valid_selections()),
        )

        self.assert_domain_error(response, 413, "FILE_TOO_LARGE")

    async def test_corrupt_image_returns_clear_error(self):
        response = await self.post_analysis(
            b"not an image",
            json.dumps(self.valid_selections()),
        )

        self.assert_domain_error(response, 400, "INVALID_FILE")

    async def test_malformed_selections_return_clear_error(self):
        for selections in ("{invalid json", json.dumps({"skin": {"x": 0, "y": 0}})):
            with self.subTest(selections=selections):
                response = await self.post_analysis(self.make_png(), selections)
                self.assert_domain_error(response, 400, "INVALID_PARAMETERS")

    async def test_last_pixel_coordinates_are_valid(self):
        response = await self.post_analysis(
            self.make_png(),
            json.dumps(self.valid_selections()),
        )

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertIn("analysis", payload)
        self.assertIn("chroma", payload["analysis"]["skin"])
        self.assertEqual(
            set(payload["analysis"]["color_ranges"]),
            {"value", "lightness"},
        )
        self.assertIn("rule_consistency", payload["seasonal_analysis"])
        self.assertNotIn("confidence", payload["seasonal_analysis"])

    async def test_coordinate_outside_image_returns_clear_error(self):
        selections = self.valid_selections()
        selections["eyes"] = {"x": 2, "y": 1}
        response = await self.post_analysis(self.make_png(), json.dumps(selections))

        self.assert_domain_error(response, 400, "INVALID_COORDINATES")


if __name__ == "__main__":
    unittest.main()
