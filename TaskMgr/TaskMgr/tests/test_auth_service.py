import io
from pathlib import Path
import unittest
from unittest.mock import patch

from auth_service import (
    build_user,
    find_user_by_username,
    load_users,
    save_users,
    validate_registration_form,
)


class AuthServiceTests(unittest.TestCase):
    def test_registration_rejects_duplicate_username_case_insensitive(self):
        errors = validate_registration_form(
            {
                "display_name": "Иван",
                "username": "ADMIN",
                "password": "1234",
                "password_repeat": "1234",
            },
            [{"username": "admin", "displayName": "Администратор", "id": "user-admin", "password": "1234"}],
        )

        self.assertIn("username", errors)

    def test_registration_rejects_missing_password_repeat(self):
        errors = validate_registration_form(
            {
                "display_name": "Иван",
                "username": "ivan",
                "password": "1234",
                "password_repeat": "",
            },
            [],
        )

        self.assertIn("password_repeat", errors)

    def test_registration_rejects_mismatched_passwords(self):
        errors = validate_registration_form(
            {
                "display_name": "Иван",
                "username": "ivan",
                "password": "1234",
                "password_repeat": "12345",
            },
            [],
        )

        self.assertIn("password_repeat", errors)

    def test_registration_accepts_valid_data(self):
        errors = validate_registration_form(
            {
                "display_name": "Иван",
                "username": "ivan_petrov",
                "password": "1234",
                "password_repeat": "1234",
            },
            [],
        )

        self.assertEqual(errors, {})

    def test_build_user_normalizes_username(self):
        user = build_user(
            {
                "display_name": "  Иван Петров  ",
                "username": "  Ivan_Petrov  ",
                "password": "1234",
            }
        )

        self.assertEqual(user["username"], "ivan_petrov")
        self.assertEqual(user["displayName"], "Иван Петров")

    def test_save_and_load_users_roundtrip(self):
        users = [
            {
                "id": "user-1",
                "username": "admin",
                "displayName": "Администратор",
                "password": "1234",
            }
        ]

        saved_buffer = io.StringIO()

        class FakeWriter:
            def __enter__(self):
                return saved_buffer

            def __exit__(self, exc_type, exc, tb):
                return False

        def fake_write_open(self, mode="r", encoding=None):
            return FakeWriter()

        with patch("auth_service.Path.open", fake_write_open):
            save_users(users, Path.cwd() / "tests" / "users-roundtrip.json")

        loaded_buffer = io.StringIO(saved_buffer.getvalue())

        class FakeReader:
            def __enter__(self):
                return loaded_buffer

            def __exit__(self, exc_type, exc, tb):
                return False

        def fake_read_open(self, mode="r", encoding=None):
            return FakeReader()

        with patch("auth_service.Path.exists", return_value=True), patch("auth_service.Path.open", fake_read_open):
            loaded = load_users(Path.cwd() / "tests" / "users-roundtrip.json")

        self.assertEqual(loaded, users)

    def test_find_user_by_username_uses_normalized_match(self):
        user = find_user_by_username(
            [{"username": "admin", "displayName": "Администратор", "id": "user-admin", "password": "1234"}],
            " ADMIN ",
        )

        self.assertIsNotNone(user)
        self.assertEqual(user["username"], "admin")


if __name__ == "__main__":
    unittest.main()
