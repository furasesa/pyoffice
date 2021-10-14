import tkinter as tk
from tkinter import ttk
from tkinter import *
from pathlib import Path
import configparser
from db.main import Database


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("pyoffice")
        self.rowconfigure(0, minsize=600, weight=1)
        self.columnconfigure(1, minsize=800, weight=1)
        # self.fr_main = tk.Frame(self)  # Right Side
        self.fr_main = ttk.Treeview(self)  # Main Class
        self.fr_menu = tk.Frame(self)  # Left Side
        self.fr_view = tk.Frame(self)  # Right Side

        # Left Side
        self.btn_product = tk.Button(self.fr_menu, text="Product")
        self.btn_customer = tk.Button(self.fr_menu, text="Customer")
        self.btn_setting = tk.Button(self.fr_menu, text="Setting")

        self.btn_product.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        self.btn_customer.grid(row=1, column=0, sticky="ew", padx=5)
        self.btn_setting.grid(row=2, column=0, sticky="ew", padx=5)

        self.fr_main.grid(row=0, column=1, sticky="nsew")
        self.fr_menu.grid(row=0, column=0, sticky="ns")
        self.fr_view.grid(row=1, column=1, sticky="ns")

        self.btn_product.bind('<Button-1>', self.product_load)

    def product_load(self, event):
        # self.tb_list = ttk.Treeview(self.fr_main)
        btn_add = tk.Button(self.fr_view, text="add")
        btn_edit = tk.Button(self.fr_view, text="edit")
        btn_delete = tk.Button(self.fr_view, text="del")

        btn_add.grid(row=0, column=2, sticky="ew", padx=5, pady=5)
        btn_edit.grid(row=0, column=1, sticky="ew", padx=5, pady=5)
        btn_delete.grid(row=0, column=0, sticky="ew", padx=5, pady=5)

        dbpath = './pyoffice.db'
        # cfgpath = './pyoffice.ini'
        # config = configparser.ConfigParser()
        # config.read(cfgpath)
        mdb = Database(dbpath)

        col = mdb.get_cursor_description("SELECT * from product")
        print(f"col : {col}")

        # self.fr_main['columns'] = ('Name', 'Gender', 'Title')
        # self.fr_main.column("#0", width=0, stretch=NO)
        # self.fr_main.column("Name", anchor=CENTER)
        # self.fr_main.column("Gender", anchor=CENTER)
        # self.fr_main.column("Title", anchor=CENTER)

        self.fr_main['columns'] = tuple(col)
        self.fr_main.column("#0", width=0, stretch=NO)
        for c in col:
            if c == 'id':
                self.fr_main.column(c, minwidth=100, width=200)
            elif c == 'price':
                self.fr_main.column(c, anchor='e', minwidth=100, width=100)
            elif c == 'name':
                self.fr_main.column(c, minwidth=200, width=300)
            else:
                self.fr_main.column(c, minwidth=100, width=100)

            self.fr_main.heading(c, text=c)

        raw = mdb.get_cursor_raw("SELECT * FROM product")

        rid = 0
        for r in raw:
            print(f"r : {r}")
            self.fr_main.insert(parent='', index='end', iid=rid, text='', values=r)
            rid += 1

        # self.fr_main.insert(parent='', index='end', iid=0, text='', values=('Todd S Core', 'Male', 'Mr'))
        # self.fr_main.insert(parent='', index='end', iid=1, text='', values=('Thomas C Wood', 'Male', 'Mr'))
        # self.fr_main.insert(parent='', index='end', iid=2, text='', values=('Misha J McKinney', 'Female', 'Mrs'))
        # self.fr_main.insert(parent='', index='end', iid=3, text='', values=('Teresa B Haight', 'Female', 'Ms'))
        # self.fr_main.insert(parent='', index='end', iid=4, text='', values=('Michael L McLaurin', 'Male', 'Mr'))
        # self.fr_main.insert(parent='', index='end', iid=5, text='', values=('David S Ward', 'Male', 'Mr'))
        # self.fr_main.insert(parent='', index='end', iid=6, text='', values=('Carolyn G Price', 'Feale', 'Mrs'))
        # self.fr_main.insert(parent='', index='end', iid=7, text='', values=('Diana D Lai', 'Female', 'Ms'))
        # self.fr_main.insert(parent='', index='end', iid=8, text='', values=('Bonnie E Duran', 'Female', 'Ms'))
        # self.fr_main.insert(parent='', index='end', iid=9, text='', values=('Joseph M Munger', 'Male', 'Mr'))


if __name__ == '__main__':
    print("test0")
    app = App()
    app.mainloop()



