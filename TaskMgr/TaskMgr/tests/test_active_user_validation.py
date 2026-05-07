# Unit-тесты проверки формы страницы "Активные пользователи".

import unittest
from datetime import date, timedelta

from active_user_service import (
    build_active_user,
    calculate_activity_score,
    is_valid_activity_date,
    is_valid_user_phone,
    validate_active_user,
)


class ActiveUserValidationTests(unittest.TestCase):
    # Создает корректный набор данных формы активного пользователя для тестов.
    # @returns словарь с валидными значениями всех обязательных полей пользователя.
    # @throws не выбрасывает исключения.
    # @note дата активности берется от текущего дня, чтобы тесты не устаревали.
    def valid_form(self):
        return {
            "nick": "active_user",
            "description": "Regular active user",
            "active_date": date.today().strftime("%Y-%m-%d"),
            "phone": "+7 (999) 123-45-67",
            "events_created": "2",
            "comments_count": "3",
            "notes_count": "4",
            "groups_joined": "1",
        }

    # Проверяет, что корректная дата активности принимается валидатором.
    # @returns None.
    # @throws AssertionError если валидатор ошибочно отклонит корректную дату.
    # @note дата должна быть в формате YYYY-MM-DD.
    def test_valid_activity_date(self):
        self.assertTrue(is_valid_activity_date(date.today().strftime("%Y-%m-%d")))

    # Проверяет, что дата активности позже текущего дня отклоняется валидатором.
    # @returns None.
    # @throws AssertionError если будущая дата ошибочно пройдет проверку.
    # @note дата строится динамически от date.today().
    def test_future_activity_date_is_invalid(self):
        tomorrow = date.today() + timedelta(days=1)

        self.assertFalse(is_valid_activity_date(tomorrow.strftime("%Y-%m-%d")))

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
            "active_date": date.today().strftime("%Y-%m-%d"),
        }

        self.assertEqual(calculate_activity_score(user), 23)

    # Проверяет, что полностью корректная форма активного пользователя не возвращает ошибок.
    # @returns None.
    # @throws AssertionError если валидная форма будет отклонена.
    # @note используется базовая форма valid_form().
    def test_valid_active_user_form_has_no_errors(self):
        errors = validate_active_user(self.valid_form(), [])

        self.assertEqual(errors, {})

    # Проверяет серверную ошибку формы активного пользователя при будущей дате.
    # @returns None.
    # @throws AssertionError если поле active_date не попадет в ошибки.
    # @note дополняет прямой тест is_valid_activity_date().
    def test_active_user_form_rejects_future_date(self):
        form = self.valid_form()
        form["active_date"] = (date.today() + timedelta(days=1)).strftime("%Y-%m-%d")

        errors = validate_active_user(form, [])

        self.assertIn("active_date", errors)

    # Проверяет, что ник активного пользователя должен быть уникальным.
    # @returns None.
    # @throws AssertionError если дубликат ника не будет найден.
    # @note сравнение ника выполняется без учета регистра.
    def test_active_user_form_rejects_duplicate_nick(self):
        form = self.valid_form()

        errors = validate_active_user(form, [{"nick": "ACTIVE_USER"}])

        self.assertIn("nick", errors)

    # Проверяет, что метрики активности не могут быть отрицательными.
    # @returns None.
    # @throws AssertionError если отрицательная метрика пройдет проверку.
    # @note ошибка должна появиться у поля events_created.
    def test_active_user_form_rejects_negative_metric(self):
        form = self.valid_form()
        form["events_created"] = "-1"

        errors = validate_active_user(form, [])

        self.assertIn("events_created", errors)

    # Проверяет, что обязательные поля активного пользователя нельзя отправить пустыми.
    # @returns None.
    # @throws AssertionError если любое обязательное поле не получит ошибку.
    # @note сценарий имитирует отправку пустой HTML-формы.
    def test_active_user_form_rejects_required_empty_fields(self):
        form = {
            "nick": "",
            "description": "",
            "active_date": "",
            "phone": "",
            "events_created": "",
            "comments_count": "",
            "notes_count": "",
            "groups_joined": "",
        }

        errors = validate_active_user(form, [])

        self.assertIn("nick", errors)
        self.assertIn("description", errors)
        self.assertIn("active_date", errors)
        self.assertIn("phone", errors)
        self.assertIn("events_created", errors)

    # Проверяет несколько независимых ошибок формы активного пользователя за один проход.
    # @returns None.
    # @throws AssertionError если ник, описание или телефон ошибочно пройдут проверку.
    # @note тест покрывает ветки формата ника, длины описания и формата телефона.
    def test_active_user_form_rejects_bad_nick_short_description_and_phone(self):
        form = self.valid_form()
        form["nick"] = "no spaces"
        form["description"] = "short"
        form["phone"] = "+7 (999) 123-45"

        errors = validate_active_user(form, [])

        self.assertIn("nick", errors)
        self.assertIn("description", errors)
        self.assertIn("phone", errors)

    # Проверяет, что метрики активности должны быть целыми числами.
    # @returns None.
    # @throws AssertionError если нечисловая метрика пройдет проверку.
    # @note ошибка должна появиться у поля comments_count.
    def test_active_user_form_rejects_non_numeric_metric(self):
        form = self.valid_form()
        form["comments_count"] = "many"

        errors = validate_active_user(form, [])

        self.assertIn("comments_count", errors)

    # Проверяет сборку объекта активного пользователя из формы.
    # @returns None.
    # @throws AssertionError если текст не обрежется или метрика не станет числом.
    # @note build_active_user вызывается после успешной validate_active_user.
    def test_build_active_user_trims_text_and_parses_metrics(self):
        form = self.valid_form()
        form["nick"] = "  active_user  "

        user = build_active_user(form)

        self.assertEqual(user["nick"], "active_user")
        self.assertEqual(user["events_created"], 2)


if __name__ == "__main__":
    unittest.main()
