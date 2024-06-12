import hashlib
from tkinter import Label, Entry, LabelFrame, W, E, END
from tkinter import ttk
from .base_page import Page
from services.user_service import UserService


class LoginPage(Page):
    def __init__(self, parent, login_success_callback, *args, **kwargs):
        Page.__init__(self, parent, *args, **kwargs)
        self.login_success_callback = login_success_callback

        # Login page tab text
        frame = LabelFrame(self, text="Login")
        frame.grid(row=0, column=0, columnspan=3, pady=20)

        # Input name
        Label(frame, text="Name: ").grid(row=1, column=0)
        self.name = Entry(frame)
        self.name.focus()
        self.name.grid(row=1, column=1)

        # Input password
        Label(frame, text="Password: ").grid(row=2, column=0)
        self.password = Entry(frame, show="*")
        self.password.grid(row=2, column=1)

        # Login button
        ttk.Button(frame, text="Login", command=self.auth_login).grid(
            row=3, columnspan=2, sticky=W + E
        )

        # Output message
        self.message = Label(self, text="", fg="red")
        self.message.grid(row=4, column=0, columnspan=2, sticky=W + E)

    def auth_login(self):
        # Get input values
        name = self.name.get()
        password = self.password.get()

        # Hash user password
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        # Tuple values
        response_data = UserService.get_login(parameters=(name, hashed_password))

        if response_data:
            self.login_success_callback(response_data)
        else:
            self.message["text"] = "Invalid username or password"
        self.name.delete(0, END)
        self.password.delete(0, END)
