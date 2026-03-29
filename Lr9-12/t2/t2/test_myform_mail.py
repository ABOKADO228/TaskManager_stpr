import unittest
from myform_mail import is_valid_email


class TestEmailValidation(unittest.TestCase):

    def test_invalid_email_assert_false(self):
        list_mail_uncor = [
            "",                     # пустая строка
            "1",                    # вообще не email
            "m1@",                  # нет домена
            "@mail.ru",             # нет локальной части
            "mail.ru",              # нет @
            "m..m@mail.ru",         # две точки подряд в локальной части
            ".m@mail.ru",           # точка в начале локальной части
            "m.@mail.ru",           # точка в конце локальной части
            "m@mail",               # нет доменной зоны
            "m@mail.",              # домен оканчивается точкой
            "m@.ru",                # домен начинается с точки
            "m@mail..ru",           # две точки подряд в домене
            "m@ma_il.ru",           # недопустимый символ _ в домене
            "m mail@mail.ru",       # пробел в локальной части
            "m@mail,ru",            # запятая вместо точки
            "маша@mail.ru",         # кириллица в локальной части
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