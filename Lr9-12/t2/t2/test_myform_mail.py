import unittest
from myform_mail import is_valid_email


class TestEmailValidation(unittest.TestCase):

    def test_invalid_email_assert_false(self):
        list_mail_uncor = [
            "",
            "1",
            "m1@",
            "@mail.ru",
            "mail.ru",
            "m..m@mail.ru",
            ".m@mail.ru",
            "m.@mail.ru",
            "m@mail",
            "m@mail.",
            "m@.ru",
            "m@mail..ru",
            "m@ma_il.ru",
            "m mail@mail.ru",
            "m@mail,ru",
            "маша@mail.ru",
        ]

        for mail in list_mail_uncor:
            with self.subTest(mail=mail):
                self.assertFalse(is_valid_email(mail))

    def test_valid_email_assert_true(self):
        list_mail_cor = [
            "m.m@mail.ru",
            "m1@gmail.com",
            "user123@yandex.ru",
            "test-email@mail.com",
            "name_surname@mail.org",
            "a.b-c_d@mail.co.uk",
            "abc123@sub.domain.net",
            "simple@example.com",
            "my.mail+box@gmail.com",
            "user-name@domain.kz",
        ]

        for mail in list_mail_cor:
            with self.subTest(mail=mail):
                self.assertTrue(is_valid_email(mail))


if __name__ == "__main__":
    unittest.main()