import tkinter as tk
from tkinter import *
from tkinter import ttk
from ..db.main import Database


class App(tk.Tk):
    def __init__(self, database):
        super().__init__()
        self.title("pyoffice")
        self.rowconfigure(0, minsize=600, weight=1)
        self.columnconfigure(1, minsize=800, weight=1)

        self.fr_main = tk.Frame(self)  # Right Side
        # self.tb_list = ttk.Treeview(self)
        self.fr_buttons = tk.Frame(self)  # Left Side

        # Left Side
        self.btn_home = tk.Button(self.fr_buttons, text="Home")
        self.btn_customer = tk.Button(self.fr_buttons, text="Customer", command=self.customer_layout)
        self.btn_setting = tk.Button(self.fr_buttons, text="Setting")

        self.btn_home.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        self.btn_customer.grid(row=1, column=0, sticky="ew", padx=5)
        self.btn_setting.grid(row=2, column=0, sticky="ew", padx=5)

        self.fr_buttons.grid(row=0, column=0, sticky="ns")
        self.fr_main.grid(row=0, column=1, sticky="nsew")

        self.mdb = Database(database)

    def create_table(self, cols, rows):
        tbl = ttk.Treeview(self, column=cols)
        num = 0
        for name in cols:
            tbl.column(f"#{num}", anchor=CENTER)
            tbl.heading(f"{num}", text=f"{name}")
            num += 1

        num = 0
        for row in rows:
            tbl.insert(parent=self.fr_main, index='end', iid=num, values=row)
            num += 1

        tbl.pack()


    def customer_layout(self):
        lst_data = self.mdb.get_cursor_data("SELECT name FROM lt")
        lst_raw = self.mdb.get_cursor_raw("SELECT * FROM lt WHERE id==\'md\'")
        lst_desc = (self.mdb.get_cursor_description("SELECT * FROM lt"))

        print(f"lst data {type(lst_data)}:\n{lst_data}\n")
        print(f"lst desc {type(lst_desc)}:\n{lst_desc}\n")

        self.create_table(lst_desc, lst_raw)
