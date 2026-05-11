# Unit-тесты проверки формы страницы "Активные пользователи".

import unittest
from datetime import date, timedelta

from active_user_service import (
    build_active_user,
    calculate_activity_score,
    is_valid_activity_date,
    is_valid_metric,
    is_valid_user_description,
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

    # Проверяет разные варианты даты последней активности.
    # @returns None.
    # @throws AssertionError если валидатор даты ошибочно примет или отклонит значение.
    # @note HTML-поле type=date отправляет дату в формате YYYY-MM-DD.
    def test_activity_date_validation_cases(self):
        cases = [
            (date.today().strftime("%Y-%m-%d"), True),
            ((date.today() + timedelta(days=1)).strftime("%Y-%m-%d"), False),
            ("04.05.2026", False),
            ("2026-02-30", False),
            ("2024-02-29", True),
        ]

        for value, expected in cases:
            with self.subTest(value=value):
                self.assertEqual(is_valid_activity_date(value), expected)

    # Проверяет разные варианты телефона пользователя.
    # @returns None.
    # @throws AssertionError если валидатор телефона ошибочно примет или отклонит значение.
    # @note российский номер должен содержать 11 цифр и начинаться с 7 или 8.
    def test_user_phone_validation_cases(self):
        cases = [
            ("+7 (999) 123-45-67", True),
            ("8 999 123-45-67", True),
            ("555-12", False),
            ("+1 (999) 123-45-67", False),
            ("+7 abc 123-45-67", False),
            ("+7 (999) 123-45-67-89", False),
        ]

        for value, expected in cases:
            with self.subTest(value=value):
                self.assertEqual(is_valid_user_phone(value), expected)

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

    # Проверяет, что испорченные или отрицательные метрики считаются как 0.
    # @returns None.
    # @throws AssertionError если невалидные метрики повлияют на рейтинг.
    # @note parse_metric защищает расчет рейтинга от поврежденных данных в JSON.
    def test_activity_score_clamps_invalid_metrics_to_zero(self):
        user = {
            "events_created": "bad",
            "comments_count": -5,
            "notes_count": None,
            "groups_joined": 1,
            "active_date": date.today().strftime("%Y-%m-%d"),
        }

        self.assertEqual(calculate_activity_score(user), 5)

    # Проверяет разные варианты метрик активности.
    # @returns None.
    # @throws AssertionError если валидатор метрик ошибочно примет или отклонит значение.
    # @note метрики должны быть непустыми неотрицательными целыми числами.
    def test_metric_validation_cases(self):
        cases = [
            ("0", True),
            ("10", True),
            ("", False),
            ("-1", False),
            ("many", False),
            ("1.5", False),
        ]

        for value, expected in cases:
            with self.subTest(value=value):
                self.assertEqual(is_valid_metric(value), expected)

    # Проверяет разные варианты описания пользователя.
    # @returns None.
    # @throws AssertionError если проверка описания ошибочно примет или отклонит значение.
    # @note описание должно содержать минимум 2 слова, 5 букв и разные символы.
    def test_user_description_validation_cases(self):
        cases = [
            ("Пользователь активно участвует", True),
            ("Студент 2 курса активно пишет комментарии", True),
            ("1234567890", False),
            ("----------", False),
            ("!!!!!!!!!!", False),
            ("аааааааааа", False),
            ("test", False),
            ("актив", False),
            ("12345 актив", False),
        ]

        for value, expected in cases:
            with self.subTest(value=value):
                self.assertEqual(is_valid_user_description(value), expected)

    # Проверяет, что полностью корректная форма активного пользователя не возвращает ошибок.
    # @returns None.
    # @throws AssertionError если валидная форма будет отклонена.
    # @note используется базовая форма valid_form().
    def test_valid_active_user_form_has_no_errors(self):
        errors = validate_active_user(self.valid_form(), [])

        self.assertEqual(errors, {})

    # Проверяет ошибки формы активного пользователя для разных невалидных дат.
    # @returns None.
    # @throws AssertionError если поле active_date не попадет в ошибки.
    # @note дополняет прямую проверку is_valid_activity_date().
    def test_active_user_form_rejects_invalid_activity_date_cases(self):
        cases = [
            (date.today() + timedelta(days=1)).strftime("%Y-%m-%d"),
            "04.05.2026",
            "2026-02-30",
            "",
        ]

        for value in cases:
            with self.subTest(value=value):
                form = self.valid_form()
                form["active_date"] = value

                errors = validate_active_user(form, [])

                self.assertIn("active_date", errors)

    # Проверяет разные ошибки ника активного пользователя.
    # @returns None.
    # @throws AssertionError если поле nick ошибочно пройдет проверку.
    # @note формат ника задается регулярным выражением в validate_active_user.
    def test_active_user_form_rejects_invalid_nick_cases(self):
        cases = [
            "",
            "ab",
            "a" * 25,
            "no spaces",
            "bad@nick",
        ]

        for value in cases:
            with self.subTest(value=value):
                form = self.valid_form()
                form["nick"] = value

                errors = validate_active_user(form, [])

                self.assertIn("nick", errors)

    # Проверяет, что допустимые варианты ника принимаются формой.
    # @returns None.
    # @throws AssertionError если валидатор ошибочно отклонит разрешенный ник.
    # @note ник может содержать буквы, цифры, точку, дефис и подчеркивание.
    def test_active_user_form_accepts_valid_nick_cases(self):
        cases = [
            "active_user",
            "User-1",
            "user.name",
            "Пользователь-1",
        ]

        for value in cases:
            with self.subTest(value=value):
                form = self.valid_form()
                form["nick"] = value

                errors = validate_active_user(form, [])

                self.assertNotIn("nick", errors)

    # Проверяет, что ник активного пользователя должен быть уникальным.
    # @returns None.
    # @throws AssertionError если дубликат ника не будет найден.
    # @note сравнение ника выполняется без учета регистра.
    def test_active_user_form_rejects_duplicate_nick(self):
        form = self.valid_form()

        errors = validate_active_user(form, [{"nick": "ACTIVE_USER"}])

        self.assertIn("nick", errors)

    # Проверяет разные ошибки телефона активного пользователя на уровне всей формы.
    # @returns None.
    # @throws AssertionError если поле phone ошибочно пройдет проверку.
    # @note тест проверяет подключение is_valid_user_phone к validate_active_user.
    def test_active_user_form_rejects_invalid_phone_cases(self):
        cases = [
            "",
            "+7 (999) 123-45",
            "+1 (999) 123-45-67",
            "+7 abc 123-45-67",
            "+7 (999) 123-45-67-89",
        ]

        for value in cases:
            with self.subTest(value=value):
                form = self.valid_form()
                form["phone"] = value

                errors = validate_active_user(form, [])

                self.assertIn("phone", errors)

    # Проверяет разные ошибки описания активного пользователя на уровне всей формы.
    # @returns None.
    # @throws AssertionError если поле description ошибочно пройдет проверку.
    # @note тест проверяет длину описания и подключение is_valid_user_description.
    def test_active_user_form_rejects_invalid_description_cases(self):
        cases = [
            "",
            "short",
            "1234567890",
            "----------",
            "!!!!!!!!!!",
            "аааааааааа",
            "test",
            "12345 актив",
        ]

        for value in cases:
            with self.subTest(value=value):
                form = self.valid_form()
                form["description"] = value

                errors = validate_active_user(form, [])

                self.assertIn("description", errors)

    # Проверяет, что описание с нормальным текстом и цифрами принимается.
    # @returns None.
    # @throws AssertionError если валидатор ошибочно отклонит осмысленное описание.
    # @note цифры допустимы, когда они являются частью нормального текста.
    def test_active_user_form_accepts_description_with_text_and_digits(self):
        form = self.valid_form()
        form["description"] = "Студент 2 курса активно пишет комментарии"

        errors = validate_active_user(form, [])

        self.assertNotIn("description", errors)

    # Проверяет разные ошибки метрик активности на уровне всей формы.
    # @returns None.
    # @throws AssertionError если невалидная метрика пройдет проверку.
    # @note каждая метрика должна быть неотрицательным целым числом.
    def test_active_user_form_rejects_invalid_metric_cases(self):
        cases = [
            ("events_created", "-1"),
            ("comments_count", "many"),
            ("notes_count", ""),
            ("groups_joined", "1.5"),
        ]

        for field, value in cases:
            with self.subTest(field=field, value=value):
                form = self.valid_form()
                form[field] = value

                errors = validate_active_user(form, [])

                self.assertIn(field, errors)

    # Проверяет, что форма принимает нулевые метрики.
    # @returns None.
    # @throws AssertionError если валидатор ошибочно отклонит любую нулевую метрику.
    # @note пользователь может быть сохранен, даже если часть активности равна нулю.
    def test_active_user_form_accepts_zero_metrics(self):
        form = self.valid_form()
        form["events_created"] = "0"
        form["comments_count"] = "0"
        form["notes_count"] = "0"
        form["groups_joined"] = "0"

        errors = validate_active_user(form, [])

        self.assertNotIn("events_created", errors)
        self.assertNotIn("comments_count", errors)
        self.assertNotIn("notes_count", errors)
        self.assertNotIn("groups_joined", errors)

    # Проверяет, что пробелы вокруг числовых метрик не ломают форму.
    # @returns None.
    # @throws AssertionError если валидатор ошибочно отклонит число с пробелами.
    # @note validate_active_user обрезает пробелы перед проверкой метрики.
    def test_active_user_form_accepts_metric_with_spaces(self):
        form = self.valid_form()
        form["events_created"] = " 2 "

        errors = validate_active_user(form, [])

        self.assertNotIn("events_created", errors)

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
        self.assertIn("comments_count", errors)
        self.assertIn("notes_count", errors)
        self.assertIn("groups_joined", errors)

    # Проверяет несколько независимых ошибок формы активного пользователя за один проход.
    # @returns None.
    # @throws AssertionError если ник, описание или телефон ошибочно пройдут проверку.
    # @note тест покрывает одновременное появление нескольких ошибок формы.
    def test_active_user_form_rejects_multiple_errors_at_once(self):
        form = self.valid_form()
        form["nick"] = "no spaces"
        form["description"] = "short"
        form["phone"] = "+7 (999) 123-45"
        form["comments_count"] = "many"

        errors = validate_active_user(form, [])

        self.assertIn("nick", errors)
        self.assertIn("description", errors)
        self.assertIn("phone", errors)
        self.assertIn("comments_count", errors)

    # Проверяет сборку объекта активного пользователя из формы.
    # @returns None.
    # @throws AssertionError если текст не обрежется или метрика не станет числом.
    # @note build_active_user вызывается после успешной validate_active_user.
    def test_build_active_user_trims_text_and_parses_metrics(self):
        form = self.valid_form()
        form["nick"] = "  active_user  "
        form["description"] = "  Regular active user  "
        form["phone"] = "  +7 (999) 123-45-67  "

        user = build_active_user(form)

        self.assertEqual(user["nick"], "active_user")
        self.assertEqual(user["description"], "Regular active user")
        self.assertEqual(user["phone"], "+7 (999) 123-45-67")
        self.assertEqual(user["events_created"], 2)
        self.assertEqual(user["comments_count"], 3)
        self.assertEqual(user["notes_count"], 4)
        self.assertEqual(user["groups_joined"], 1)


if __name__ == "__main__":
    unittest.main()