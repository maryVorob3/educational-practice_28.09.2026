import math
import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox


def init_db():
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE partner_types (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type_name TEXT NOT NULL
        );
    """)
    cursor.executemany(
        "INSERT INTO partner_types (type_name) VALUES (?);",
        [("ЗАО",), ("ООО",), ("ПАО",)]
    )
    cursor.execute("""
        CREATE TABLE partners (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            FOREIGN KEY (type_id) REFERENCES partner_types(id)
        );
    """)
    cursor.execute(
        "INSERT INTO partners (type_id, name) VALUES (2, 'Паркет 29');"
    )
    cursor.execute("""
        CREATE TABLE products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_name TEXT NOT NULL
        );
    """)
    cursor.executemany(
        "INSERT INTO products (product_name) VALUES (?);",
        [("Паркетная доска Ясень",), ("Ламинат Дуб Дублин",)]
    )
    cursor.execute("""
        CREATE TABLE partner_sales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            partner_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            sale_date TEXT NOT NULL,
            FOREIGN KEY (partner_id) REFERENCES partners(id),
            FOREIGN KEY (product_id) REFERENCES products(id)
        );
    """)
    cursor.executemany("""
        INSERT INTO partner_sales (partner_id, product_id, quantity, sale_date)
        VALUES (?, ?, ?, ?);
    """, [
        (1, 1, 1550, "2026-08-12"),
        (1, 2, 820, "2026-09-01")
    ])
    conn.commit()
    return conn


class PartnerHistoryWindow(tk.Toplevel):
    def __init__(self, parent, db_conn, partner_id, partner_name):
        super().__init__(parent)
        self.parent = parent
        self.conn = db_conn
        self.partner_id = partner_id
        
        self.title(f"CRM: История реализации продукции — {partner_name}")
        self.geometry("680x450")
        self.configure(bg="#F4F4F4")
        
        self.transient(parent)
        self.grab_set()
        
        self.create_header(partner_name)
        self.create_table()
        self.load_history_data()

    def create_header(self, partner_name):
        header_frame = tk.Frame(self, bg="#FFFFFF", padx=15, pady=10, bd=1, relief="solid")
        header_frame.pack(fill="x", side="top")
        
        logo_canvas = tk.Canvas(header_frame, width=36, height=36, bg="#67BA80", highlightthickness=0)
        logo_canvas.pack(side="left", padx=(0, 10))
        logo_canvas.create_oval(4, 4, 32, 32, fill="#FFFFFF", outline="")
        logo_canvas.create_text(18, 18, text="МП", font=("Segoe UI", 9, "bold"), fill="#67BA80")
        
        title_label = tk.Label(
            header_frame,
            text=f"История реализации: {partner_name}",
            font=("Segoe UI", 12, "bold"),
            bg="#FFFFFF",
            fg="#222222"
        )
        title_label.pack(side="left")

    def create_table(self):
        container = tk.Frame(self, bg="#F4F4F4", padx=15, pady=15)
        container.pack(fill="both", expand=True)
        
        columns = ("product_name", "quantity", "sale_date")
        self.tree = ttk.Treeview(container, columns=columns, show="headings", height=12)
        
        self.tree.heading("product_name", text="Наименование продукции")
        self.tree.heading("quantity", text="Количество (шт.)")
        self.tree.heading("sale_date", text="Дата продажи")
        
        self.tree.column("product_name", width=320, anchor="w")
        self.tree.column("quantity", width=140, anchor="center")
        self.tree.column("sale_date", width=140, anchor="center")
        
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def load_history_data(self):
        cursor = self.conn.cursor()
        query = """
            SELECT pr.product_name, ps.quantity, ps.sale_date
            FROM partner_sales ps
            JOIN products pr ON ps.product_id = pr.id
            WHERE ps.partner_id = ?
            ORDER BY ps.sale_date DESC;
        """
        cursor.execute(query, (self.partner_id,))
        rows = cursor.fetchall()
        
        for row in rows:
            self.tree.insert("", "end", values=(row[0], f"{row[1]:,} шт.", row[2]))


if __name__ == "__main__":
    db = init_db()
    root = tk.Tk()
    root.withdraw()
    win = PartnerHistoryWindow(root, db, 1, "Паркет 29")
    root.mainloop()
