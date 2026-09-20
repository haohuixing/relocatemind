import unittest

from fastapi.testclient import TestClient

from app.main import app


class DiscoveryRouteTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    def test_homepage_includes_baseline_security_headers(self):
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["x-content-type-options"], "nosniff")
        self.assertEqual(response.headers["x-frame-options"], "DENY")

    def test_invalid_match_input_redirects_without_setting_assessment(self):
        response = self.client.post(
            "/match",
            data={"passport_country": "United States", "monthly_income": "not-a-number"},
            follow_redirects=False,
        )

        # FastAPI rejects malformed typed form fields before the handler executes.
        self.assertEqual(response.status_code, 422)
        self.assertNotIn("anon_test_data=", response.headers.get("set-cookie", ""))

    def test_semantically_invalid_match_redirects_without_setting_assessment(self):
        response = self.client.post(
            "/match",
            data={
                "passport_country": "United States",
                "monthly_income": "4000",
                "income_type": "unsupported",
                "savings": "15000",
                "dependents": "solo",
                "region": "any",
                "priority": "quality_of_life",
            },
            follow_redirects=False,
        )

        self.assertEqual(response.status_code, 303)
        self.assertEqual(response.headers["location"], "/free-test?error=invalid_input")

    def test_valid_match_sets_small_validated_assessment_cookie(self):
        response = self.client.post(
            "/match",
            data={
                "passport_country": "United States",
                "monthly_income": "4000",
                "income_type": "remote_work",
                "savings": "15000",
                "dependents": "solo",
                "region": "any",
                "priority": "quality_of_life",
                "timeline": "exploring",
            },
            follow_redirects=False,
        )

        self.assertEqual(response.status_code, 303)
        self.assertEqual(response.headers["location"], "/results")
        cookie = response.headers.get("set-cookie", "")
        self.assertIn("anon_test_data=", cookie)
        self.assertIn("HttpOnly", cookie)
        self.assertNotIn("matches", cookie)

        results = self.client.get("/results")
        self.assertEqual(results.status_code, 200)
        self.assertIn("Your Relocation Match Results", results.text)


if __name__ == "__main__":
    unittest.main()
