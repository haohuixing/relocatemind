import unittest

from pydantic import ValidationError

from app.models.profile import AssessmentInput
from app.modules.discovery.service import calculate_matches_for_assessment


class AssessmentContractTests(unittest.TestCase):
    def make_assessment(self, **overrides):
        values = {
            "passport_country": "United States",
            "monthly_income": 4000,
            "income_type": "remote_work",
            "savings": 15000,
            "dependents": "solo",
            "region": "any",
            "climate": "any",
            "priority": "quality_of_life",
            "timeline": "exploring",
        }
        values.update(overrides)
        return AssessmentInput.model_validate(values)

    def test_valid_assessment_returns_versioned_validated_matches(self):
        snapshot = calculate_matches_for_assessment(self.make_assessment())

        self.assertTrue(snapshot.matches)
        self.assertEqual(snapshot.matcher_version, "deterministic-v1")
        self.assertEqual(len(snapshot.program_data_version), 16)
        self.assertTrue(all(0 <= match.score <= 100 for match in snapshot.matches))
        self.assertTrue(all(match.country_id for match in snapshot.matches))

    def test_invalid_values_are_rejected(self):
        with self.assertRaises(ValidationError):
            self.make_assessment(monthly_income=0)

        with self.assertRaises(ValidationError):
            self.make_assessment(income_type="not-a-supported-income-type")

        with self.assertRaises(ValidationError):
            self.make_assessment(unexpected_field="must-be-rejected")

    def test_eu_passport_keeps_matcher_behavior_through_service(self):
        snapshot = calculate_matches_for_assessment(
            self.make_assessment(passport_country="Germany")
        )
        eu_freedom_matches = [match for match in snapshot.matches if match.is_eu_freedom]

        self.assertTrue(eu_freedom_matches)
        self.assertTrue(all(match.min_income_usd == 0 for match in eu_freedom_matches))


if __name__ == "__main__":
    unittest.main()
