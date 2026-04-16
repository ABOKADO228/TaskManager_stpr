import unittest
from authorization_test_utils import validate_email, validate_login, is_valid_question


class TestValidators(unittest.TestCase):

    # ===== EMAIL =====
    def test_email_valid(self):
        self.assertTrue(validate_email("user@example.com"))

    def test_email_no_at(self):
        self.assertFalse(validate_email("userexample.com"))

    def test_email_no_domain(self):
        self.assertFalse(validate_email("user@"))

    def test_email_with_spaces(self):
        self.assertFalse(validate_email(" user@example.com "))


    # ===== LOGIN =====
    def test_login_valid(self):
        self.assertTrue(validate_login("Ivan"))

    def test_login_too_short(self):
        self.assertFalse(validate_login("A"))

    def test_login_with_digits(self):
        self.assertFalse(validate_login("Ivan123"))

    def test_login_with_symbols(self):
        self.assertFalse(validate_login("Ivan_petrov"))


    # ===== QUESTION =====
    def test_question_valid(self):
        self.assertTrue(is_valid_question("How are you?"))

    def test_question_too_short(self):
        self.assertFalse(is_valid_question("abc"))

    def test_question_digits_only(self):
        self.assertFalse(is_valid_question("12345"))

    def test_question_spaces_and_digits(self):
        self.assertFalse(is_valid_question("   12   "))


if __name__ == "__main__":
    unittest.main()