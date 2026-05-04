# Unit-тесты проверки формы страницы "Активные пользователи".

import unittest

from active_user_service import calculate_activity_score, is_valid_activity_date, is_valid_user_phone


class ActiveUserValidationTests(unittest.TestCase):
    # Проверяет, что корректная дата активности принимается валидатором.
    # @returns None.
    # @throws AssertionError если валидатор ошибочно отклонит корректную дату.
    # @note дата должна быть в формате YYYY-MM-DD.
    def test_valid_activity_date(self):
        self.assertTrue(is_valid_activity_date("2026-05-04"))

    # Проверяет, что дата с точками не проходит валидацию.
    # @returns None.
    # @throws AssertionError если валидатор ошибочно примет формат DD.MM.YYYY.
    # @note HTML-поле type=date отправляет дату в формате YYYY-MM-DD.
    def test_invalid_activity_date_format(self):
        self.assertFalse(is_valid_activity_date("04.05.2026"))

    # Проверяет, что российский телефон с разделителями принимается.
    # @returns None.
    # @throws AssertionError если валидатор ошибочно отклонит корректный телефон.
    # @note скобки, пробелы и дефисы допустимы для удобства пользователя.
    def test_valid_user_phone(self):
        self.assertTrue(is_valid_user_phone("+7 (999) 123-45-67"))

    # Проверяет, что слишком короткий телефон отклоняется.
    # @returns None.
    # @throws AssertionError если валидатор ошибочно примет короткий номер.
    # @note после удаления нецифровых символов в номере должно быть 11 цифр.
    def test_invalid_user_phone(self):
        self.assertFalse(is_valid_user_phone("555-12"))

    # Проверяет расчет рейтинга активности по метрикам пользователя.
    # @returns None.
    # @throws AssertionError если формула рейтинга изменилась неожиданно.
    # @note формула: события*4 + комментарии*2 + заметки + группы*3 + свежая дата.
    def test_activity_score_uses_user_metrics(self):
        user = {
            "events_created": 2,
            "comments_count": 3,
            "notes_count": 4,
            "groups_joined": 1,
            "active_date": "2026-05-04",
        }

        self.assertEqual(calculate_activity_score(user), 23)


if __name__ == "__main__":
    unittest.main()
