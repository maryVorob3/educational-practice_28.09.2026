import datetime
import logging
import math
import sqlite3
import unittest



logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    encoding="utf-8"
)

PRODUCT_TYPE_COEFFICIENTS = {1: 1.1, 2: 2.5, 3: 8.43}
MATERIAL_TYPE_DEFECTS = {1: 0.3, 2: 0.12}


def calculate_material_consumption(product_type_id, material_type_id, quantity, param_1, param_2):
    try:
        if not isinstance(product_type_id, int) or not isinstance(material_type_id, int):
            raise ValueError("ID типов должны быть целыми числами")
        if not isinstance(quantity, int) or not isinstance(param_1, (int, float)) or not isinstance(param_2, (int, float)):
            raise ValueError("Параметры количества и размеров имеют неверный тип")

        if quantity <= 0 or param_1 <= 0 or param_2 <= 0:
            raise ValueError("Параметры должны быть больше нуля")

        if product_type_id not in PRODUCT_TYPE_COEFFICIENTS or material_type_id not in MATERIAL_TYPE_DEFECTS:
            raise ValueError("Несуществующий ID типа продукции или материала")

        product_coefficient = PRODUCT_TYPE_COEFFICIENTS[product_type_id]
        defect_percent = MATERIAL_TYPE_DEFECTS[material_type_id]

        base_consumption = param_1 * param_2 * product_coefficient
        total_clean_consumption = base_consumption * quantity
        total_with_defect = total_clean_consumption * (1.0 + (defect_percent / 100.0))

        return math.ceil(total_with_defect)

    except Exception as err:
        logging.error(f"Ошибка в методе расчета материалов: {str(err)}")
        return -1


def safe_get_partner_by_id(cursor, partner_id):
    """Безопасный параметризованный запрос без SQL-инъекций"""
    query = "SELECT id, name FROM partners WHERE id = ?"
    cursor.execute(query, (partner_id,))
    return cursor.fetchone()


class TestMaterialCalculation(unittest.TestCase):
    def test_1_standard_calculation(self):
        """Тест 1: Стандартный корректный расчет"""
        res = calculate_material_consumption(1, 1, 10, 1.5, 2.0)
        self.assertEqual(res, 34)

    def test_2_rounding_up(self):
        """Тест 2: Округление строго в большую сторону"""
        res = calculate_material_consumption(1, 2, 1, 1.0, 1.0)
        self.assertEqual(res, 2)

    def test_3_nonexistent_type_id(self):
        """Тест 3: Несуществующий тип продукции или материала"""
        res = calculate_material_consumption(99, 1, 10, 1.5, 2.0)
        self.assertEqual(res, -1)

    def test_4_negative_parameters(self):
        """Тест 4: Отрицательные размеры param_1 или param_2"""
        res = calculate_material_consumption(1, 1, 10, -1.5, 2.0)
        self.assertEqual(res, -1)

    def test_5_zero_or_negative_quantity(self):
        """Тест 5: Нулевое или отрицательное количество продукции"""
        res = calculate_material_consumption(1, 1, 0, 1.5, 2.0)
        self.assertEqual(res, -1)


if __name__ == "__main__":
    unittest.main()
