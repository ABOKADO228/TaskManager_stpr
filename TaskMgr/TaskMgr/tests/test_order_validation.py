# Unit-тесты проверки формы страницы "Оформленные заказы".

import unittest

from order_service import build_order, filter_orders_for_user, is_valid_order_date, is_valid_phone


class OrderValidationTests(unittest.TestCase):
    # Проверяет, что корректная дата заказа принимается валидатором.
    # @returns None.
    # @throws AssertionError если валидатор ошибочно отклонит корректную дату.
    # @note дата должна быть в формате YYYY-MM-DD.
    def test_valid_order_date(self):
        self.assertTrue(is_valid_order_date("2026-05-01"))

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
            "date": "2026-05-01",
            "phone": "+7 (999) 123-45-67",
        }
        owner = {"id": "user-admin", "display_name": "Администратор"}

        order = build_order(form, owner)

        self.assertEqual(order["owner_id"], "user-admin")
        self.assertEqual(order["owner_name"], "Администратор")


if __name__ == "__main__":
    unittest.main()
