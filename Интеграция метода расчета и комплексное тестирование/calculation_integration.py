import math
import tkinter as tk
from tkinter import ttk, messagebox


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
    if not isinstance(product_type_id, int) or not isinstance(material_type_id, int):
        return -1
    if not isinstance(quantity, int) or not isinstance(param_1, (int, float)) or not isinstance(param_2, (int, float)):
        return -1

    if quantity <= 0 or param_1 <= 0 or param_2 <= 0:
        return -1

    if product_type_id not in PRODUCT_TYPE_COEFFICIENTS or material_type_id not in MATERIAL_TYPE_DEFECTS:
        return -1

    product_coefficient = PRODUCT_TYPE_COEFFICIENTS[product_type_id]
    defect_percent = MATERIAL_TYPE_DEFECTS[material_type_id]

    base_consumption = param_1 * param_2 * product_coefficient
    total_clean_consumption = base_consumption * quantity
    total_with_defect = total_clean_consumption * (1.0 + (defect_percent / 100.0))

    return math.ceil(total_with_defect)


class MaterialCalculatorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("CRM: Калькулятор расчета материалов")
        self.geometry("450x520")
        self.configure(bg="#F4F4F4")

        self.create_widgets()

    def create_widgets(self):
        header = tk.Frame(self, bg="#FFFFFF", pady=12, padx=15, bd=1, relief="solid")
        header.pack(fill="x")
        
        tk.Label(
            header,
            text="Расчет расхода сырья",
            font=("Segoe UI", 12, "bold"),
            bg="#FFFFFF",
            fg="#222222"
        ).pack(side="left")

        form = tk.Frame(self, bg="#F4F4F4", padx=20, pady=15)
        form.pack(fill="both", expand=True)

        tk.Label(form, text="Тип продукции (ID):", bg="#F4F4F4", font=("Segoe UI", 9, "bold")).pack(anchor="w")
        self.prod_combo = ttk.Combobox(form, values=["1 - Тип 1 (Коэф. 1.1)", "2 - Тип 2 (Коэф. 2.5)", "3 - Тип 3 (Коэф. 8.43)"], state="readonly")
        self.prod_combo.current(0)
        self.prod_combo.pack(fill="x", pady=(2, 8))

        tk.Label(form, text="Тип материала (ID):", bg="#F4F4F4", font=("Segoe UI", 9, "bold")).pack(anchor="w")
        self.mat_combo = ttk.Combobox(form, values=["1 - Материал 1 (Брак 0.3%)", "2 - Материал 2 (Брак 0.12%)"], state="readonly")
        self.mat_combo.current(0)
        self.mat_combo.pack(fill="x", pady=(2, 8))

        tk.Label(form, text="Количество продукции (шт.):", bg="#F4F4F4", font=("Segoe UI", 9, "bold")).pack(anchor="w")
        self.qty_entry = tk.Entry(form, font=("Segoe UI", 10))
        self.qty_entry.insert(0, "10")
        self.qty_entry.pack(fill="x", pady=(2, 8))

        tk.Label(form, text="Параметр 1 (длина/ширина):", bg="#F4F4F4", font=("Segoe UI", 9, "bold")).pack(anchor="w")
        self.p1_entry = tk.Entry(form, font=("Segoe UI", 10))
        self.p1_entry.insert(0, "1.5")
        self.p1_entry.pack(fill="x", pady=(2, 8))

        tk.Label(form, text="Параметр 2 (высота/толщина):", bg="#F4F4F4", font=("Segoe UI", 9, "bold")).pack(anchor="w")
        self.p2_entry = tk.Entry(form, font=("Segoe UI", 10))
        self.p2_entry.insert(0, "2.0")
        self.p2_entry.pack(fill="x", pady=(2, 8))

        tk.Button(
            form,
            text="Рассчитать расход",
            bg="#67BA80",
            fg="#FFFFFF",
            font=("Segoe UI", 10, "bold"),
            command=self.on_calculate
        ).pack(fill="x", pady=15)

        self.result_label = tk.Label(
            form,
            text="Результат: -",
            font=("Segoe UI", 11, "bold"),
            bg="#F4F4F4",
            fg="#222222"
        )
        self.result_label.pack(anchor="w")

    def on_calculate(self):
        try:
            prod_id = int(self.prod_combo.get().split()[0])
            mat_id = int(self.mat_combo.get().split()[0])
            qty = int(self.qty_entry.get().strip())
            p1 = float(self.p1_entry.get().strip())
            p2 = float(self.p2_entry.get().strip())
        except ValueError:
            messagebox.showwarning(
                "Ошибка ввода",
                "Пожалуйста, введите корректные числовые параметры!"
            )
            self.result_label.config(text="Результат: Ошибка ввода")
            return

        result = calculate_material_consumption(prod_id, mat_id, qty, p1, p2)

        if result == -1:
            messagebox.showwarning(
                "Некорректные параметры",
                "Метод расчета вернул -1. Проверьте правильность введенных данных."
            )
            self.result_label.config(text="Результат: Некорректные данные (-1)")
        else:
            self.result_label.config(text=f"Необходимо материала: {result} ед.")


if __name__ == "__main__":
    app = MaterialCalculatorApp()
    app.mainloop()
