# Unit-тесты проверки формы страницы "Оформленные заказы".

import unittest
from datetime import date, timedelta

from order_service import build_order, filter_orders_for_user, is_valid_order_date, is_valid_phone, validate_order


class OrderValidationTests(unittest.TestCase):
    def valid_form(self):
        return {
            "number": "ORD-10",
            "author": "Anna",
            "text": "Order description",
            "date": date.today().strftime("%Y-%m-%d"),
            "phone": "+7 (999) 123-45-67",
        }

    # Проверяет, что корректная дата заказа принимается валидатором.
    # @returns None.
    # @throws AssertionError если валидатор ошибочно отклонит корректную дату.
    # @note дата должна быть в формате YYYY-MM-DD.
    def test_valid_order_date(self):
        self.assertTrue(is_valid_order_date(date.today().strftime("%Y-%m-%d")))

    def test_future_order_date_is_invalid(self):
        tomorrow = date.today() + timedelta(days=1)

        self.assertFalse(is_valid_order_date(tomorrow.strftime("%Y-%m-%d")))

    # Проверяет, что дата с точками не проходит валидацию.
    # @returns None.
    # @throws AssertionError если валидатор ошибочно примет формат DD.MM.YYYY.
    # @note форма и сервер ожидают ISO-формат YYYY-MM-DD.
    def test_invalid_order_date_format(self):
        self.assertFalse(is_valid_order_date("01.05.2026"))

    # Проверяет, что российский телефон с разделителями принимается.
    # @returns None.
    # @throws AssertionError если валидатор ошибочно отклонит корректный телефон.
    # @note формат допускает +7, скобки, пробелы и дефисы.
    def test_valid_phone(self):
        self.assertTrue(is_valid_phone("+7 (999) 123-45-67"))

    # Проверяет, что короткий телефон отклоняется.
    # @returns None.
    # @throws AssertionError если валидатор ошибочно примет короткий номер.
    # @note валидный номер должен содержать 11 цифр и начинаться с 7 или 8.
    def test_invalid_phone(self):
        self.assertFalse(is_valid_phone("12345"))

    # Проверяет, что список заказов фильтруется по текущему пользователю.
    # @returns None.
    # @throws AssertionError если фильтр вернет чужой заказ.
    # @note используется серверным маршрутом /orders для личного кабинета.
    def test_filter_orders_for_current_user(self):
        orders = [
            {"number": "ORD-1", "owner_id": "user-admin"},
            {"number": "ORD-2", "owner_id": "user-user1"},
            {"number": "ORD-3"},
        ]

        result = filter_orders_for_user(orders, "user-admin")

        self.assertEqual([order["number"] for order in result], ["ORD-1"])

    # Проверяет, что новый заказ сохраняет владельца.
    # @returns None.
    # @throws AssertionError если build_order не добавит owner_id или owner_name.
    # @note без этих полей заказ не сможет отображаться только у своего пользователя.
    def test_build_order_adds_owner(self):
        form = {
            "number": "ORD-10",
            "author": "Анна",
            "text": "Описание заказа",
            "date": date.today().strftime("%Y-%m-%d"),
            "phone": "+7 (999) 123-45-67",
        }
        owner = {"id": "user-admin", "display_name": "Администратор"}

        order = build_order(form, owner)

        self.assertEqual(order["owner_id"], "user-admin")
        self.assertEqual(order["owner_name"], "Администратор")


    def test_valid_order_form_has_no_errors(self):
        errors = validate_order(self.valid_form(), [])

        self.assertEqual(errors, {})

    def test_order_form_rejects_future_date(self):
        form = self.valid_form()
        form["date"] = (date.today() + timedelta(days=1)).strftime("%Y-%m-%d")

        errors = validate_order(form, [])

        self.assertIn("date", errors)

    def test_order_form_rejects_duplicate_number(self):
        form = self.valid_form()

        errors = validate_order(form, [{"number": "ord-10"}])

        self.assertIn("number", errors)

    def test_order_form_rejects_short_text(self):
        form = self.valid_form()
        form["text"] = "short"

        errors = validate_order(form, [])

        self.assertIn("text", errors)

    def test_order_form_rejects_required_empty_fields(self):
        form = {
            "number": "",
            "author": "",
            "text": "",
            "date": "",
            "phone": "",
        }

        errors = validate_order(form, [])

        self.assertIn("number", errors)
        self.assertIn("author", errors)
        self.assertIn("text", errors)
        self.assertIn("date", errors)
        self.assertIn("phone", errors)

    def test_order_form_rejects_bad_number_short_author_and_phone(self):
        form = self.valid_form()
        form["number"] = "bad number"
        form["author"] = "A"
        form["phone"] = "+7 (999) 123-45"

        errors = validate_order(form, [])

        self.assertIn("number", errors)
        self.assertIn("author", errors)
        self.assertIn("phone", errors)

    def test_build_order_without_owner_uses_empty_owner_fields(self):
        order = build_order(self.valid_form())

        self.assertEqual(order["owner_id"], "")
        self.assertEqual(order["owner_name"], "")


if __name__ == "__main__":
    unittest.main()
