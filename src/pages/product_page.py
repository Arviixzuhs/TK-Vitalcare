from tkinter import *
from tkinter import ttk
from .base_page import Page
from tkinter import ttk
from utils.run_query import run_query


class ProductPage(Page):
    def __init__(self, parent, *args, **kwargs):
        Page.__init__(self, parent, *args, **kwargs)

        # Creating a Frame Container
        frame = LabelFrame(self, text="Register new Product")
        frame.grid(row=0, column=0, columnspan=3, pady=20)

        # Name Input
        Label(frame, text="Name: ").grid(row=1, column=0)
        self.name = Entry(frame)
        self.name.focus()
        self.name.grid(row=1, column=1)

        # Price Input
        Label(frame, text="Price: ").grid(row=2, column=0)
        self.price = Entry(frame)
        self.price.grid(row=2, column=1)

        # Button Add Product
        ttk.Button(frame, text="Save Product", command=self.add_product).grid(
            row=3, columnspan=2, sticky=W + E
        )

        # Output Messages
        self.message = Label(self, text="", fg="red")
        self.message.grid(row=3, column=0, columnspan=2, sticky=W + E)

        # Table
        self.tree = ttk.Treeview(self, height=10, columns=2)
        self.tree.grid(row=4, column=0, columnspan=2)
        self.tree.heading("#0", text="Name", anchor=CENTER)
        self.tree.heading("#1", text="Price", anchor=CENTER)

        # Buttons
        ttk.Button(self, text="DELETE", command=self.delete_product).grid(
            row=5, column=0, sticky=W + E
        )
        ttk.Button(self, text="EDIT", command=self.edit_product).grid(
            row=5, column=1, sticky=W + E
        )

        # Filling the Rows
        self.get_products()

    def get_products(self):
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)
        query = "SELECT * FROM product ORDER BY name DESC"
        db_rows = run_query(query)
        for row in db_rows:
            self.tree.insert("", 0, text=row[1], values=row[2])

    def validation(self):
        return len(self.name.get()) != 0 and len(self.price.get()) != 0

    def add_product(self):
        if self.validation():
            query = "INSERT INTO product VALUES(NULL, ?, ?)"
            parameters = (self.name.get(), self.price.get())
            run_query(query, parameters)
            self.message["text"] = "Product {} added Successfully".format(
                self.name.get()
            )
            self.name.delete(0, END)
            self.price.delete(0, END)
        else:
            self.message["text"] = "Name and Price is Required"
        self.get_products()

    def delete_product(self):
        self.message["text"] = ""
        try:
            self.tree.item(self.tree.selection())["text"][0]
        except IndexError as e:
            self.message["text"] = "Please select a Record"
            return
        self.message["text"] = ""
        name = self.tree.item(self.tree.selection())["text"]
        query = "DELETE FROM product WHERE name = ?"
        run_query(query, (name,))
        self.message["text"] = "Record {} deleted Successfully".format(name)
        self.get_products()

    def edit_product(self):
        self.message["text"] = ""
        try:
            self.tree.item(self.tree.selection())["values"][0]
        except IndexError as e:
            self.message["text"] = "Please, select Record"
            return

        name = self.tree.item(self.tree.selection())["text"]
        old_price = self.tree.item(self.tree.selection())["values"][0]
        self.edit_wind = Toplevel()
        self.edit_wind.title = "Edit Product"

        # New Name
        Label(self.edit_wind, text="New name:").grid(row=1, column=1)
        new_name = Entry(
            self.edit_wind,
            textvariable=StringVar(self.edit_wind, value=name),
        )
        new_name.grid(row=1, column=2)

        # New Price
        Label(self.edit_wind, text="New price:").grid(row=3, column=1)
        new_price = Entry(
            self.edit_wind,
            textvariable=StringVar(self.edit_wind, value=old_price),
        )
        new_price.grid(row=3, column=2)

        Button(
            self.edit_wind,
            text="Update",
            command=lambda: self.edit_records(
                new_name.get(), name, new_price.get(), old_price
            ),
        ).grid(row=4, column=2, sticky=W)
        self.edit_wind.mainloop()

    def edit_records(self, new_name, name, new_price, old_price):
        query = "UPDATE product SET name = ?, price = ? WHERE name = ? AND price = ?"
        parameters = (new_name, new_price, name, old_price)
        run_query(query, parameters)
        self.edit_wind.destroy()
        self.message["text"] = "Record {} updated successfully".format(name)
        self.get_products()
