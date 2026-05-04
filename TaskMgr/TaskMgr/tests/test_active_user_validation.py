"""Unit tests for active user form validation."""

import unittest

from active_user_service import is_valid_activity_date, is_valid_user_phone


class ActiveUserValidationTests(unittest.TestCase):
    """Check date and phone formats for the active users page."""

    def test_valid_activity_date(self):
        """A valid date from the past or today should be accepted."""

        self.assertTrue(is_valid_activity_date("2026-05-04"))

    def test_invalid_activity_date_format(self):
        """A date written with dots should be rejected."""

        self.assertFalse(is_valid_activity_date("04.05.2026"))

    def test_valid_user_phone(self):
        """A Russian phone number with formatting should be accepted."""

        self.assertTrue(is_valid_user_phone("+7 (999) 123-45-67"))

    def test_invalid_user_phone(self):
        """A phone number with too few digits should be rejected."""

        self.assertFalse(is_valid_user_phone("555-12"))


if __name__ == "__main__":
    unittest.main()
