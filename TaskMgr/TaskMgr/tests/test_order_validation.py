"""Unit tests for order input validation rules."""

import unittest

from order_service import is_valid_order_date, is_valid_phone


class OrderValidationTests(unittest.TestCase):
    """Check date and phone rules used by the orders form."""

    def test_valid_order_date(self):
        """A real past date in YYYY-MM-DD format should be accepted."""

        self.assertTrue(is_valid_order_date("2026-05-01"))

    def test_invalid_order_date_format(self):
        """Dates outside YYYY-MM-DD format should be rejected."""

        self.assertFalse(is_valid_order_date("01.05.2026"))

    def test_valid_phone(self):
        """A Russian phone number with separators should be accepted."""

        self.assertTrue(is_valid_phone("+7 (999) 123-45-67"))

    def test_invalid_phone(self):
        """A short phone number should be rejected."""

        self.assertFalse(is_valid_phone("12345"))


if __name__ == "__main__":
    unittest.main()
