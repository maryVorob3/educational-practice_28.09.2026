import math


PRODUCT_TYPE_COEFFICIENTS = {
    1: 1.1,
    2: 2.5,
    3: 8.43
}

MATERIAL_TYPE_DEFECTS = {
    1: 0.3,
    2: 0.12
}


def calculate_material_consumption(product_type_id, material_type_id, quantity, param_1, param_2):
    """
    Расчет необходимого количества сырья с учетом брака.
    Возвращает целое число (округление вверх) или -1 при ошибках.
    """
    
    if not isinstance(product_type_id, int) or not isinstance(material_type_id, int):
        return -1
    if not isinstance(quantity, int) or not isinstance(param_1, (int, float)) or not isinstance(param_2, (int, float)):
        return -1

    
    if quantity <= 0 or param_1 <= 0 or param_2 <= 0:
        return -1

    
    if product_type_id not in PRODUCT_TYPE_COEFFICIENTS:
        return -1
    if material_type_id not in MATERIAL_TYPE_DEFECTS:
        return -1

    
    product_coefficient = PRODUCT_TYPE_COEFFICIENTS[product_type_id]
    defect_percent = MATERIAL_TYPE_DEFECTS[material_type_id]

    
    base_consumption = param_1 * param_2 * product_coefficient
    total_clean_consumption = base_consumption * quantity

    
    total_with_defect = total_clean_consumption * (1.0 + (defect_percent / 100.0))

    
    return math.ceil(total_with_defect)


if __name__ == "__main__":
    result = calculate_material_consumption(1, 1, 10, 1.5, 2.0)
    print(f"Результат расчета: {result}")
