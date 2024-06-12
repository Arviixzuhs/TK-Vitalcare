from tkinter import Tk
from tkinter import ttk
from pages.login_page import LoginPage
from pages.welcome_page import WelcomePage
from pages.product_page import ProductPage
from pages.register_page import RegisterPage
from pages.profile_page import ProfilePage
from db.db_createTables import dbCreateTables


# Default auth pages
class AuthApplication:
    def __init__(self, root):
        self.root = root
        self.root.title("Authentication")

        # Create inital notebook
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(pady=10, expand=True)

        # Initial login page
        self.login_page = LoginPage(self.notebook, self.login_success)
        self.notebook.add(self.login_page, text="Login")

        # Initial register page
        self.register_page = RegisterPage(self.notebook)
        self.notebook.add(self.register_page, text="Register")

    # Login success callback
    def login_success(self, user):
        self.root.destroy()
        main_window = Tk()
        MainApplication(main_window, user)
        main_window.mainloop()


class MainApplication:
    def __init__(self, root, user):
        self.root = root
        self.root.title("Application with Tabs")

        # Create inital notebook
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(pady=10, expand=True)

        # Welcome page
        self.welcome_page = WelcomePage(self.notebook)
        self.notebook.add(self.welcome_page, text=f"Welcome {user[1]}")

        # Product page
        self.product_page = ProductPage(self.notebook)
        self.notebook.add(self.product_page, text="Products")

        # Profile page
        self.profile_page = ProfilePage(self.notebook, user)
        self.notebook.add(self.profile_page, text="Profile")


if __name__ == "__main__":
    dbCreateTables()
    window = Tk()
    app = AuthApplication(window)
    window.mainloop()
