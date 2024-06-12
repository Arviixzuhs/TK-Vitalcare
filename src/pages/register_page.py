import hashlib
from tkinter import ttk, Label, Entry, LabelFrame, W, E, END
from pages.base_page import Page
from services.user_service import UserService


class RegisterPage(Page):
    def __init__(self, parent, *args, **kwargs):
        Page.__init__(self, parent, *args, **kwargs)

        # Register page tab text
        frame = LabelFrame(self, text="Register")
        frame.grid(row=0, column=0, columnspan=3, pady=20)

        # Input name
        Label(frame, text="Name: ").grid(row=1, column=0)
        self.name = Entry(frame)
        self.name.focus()
        self.name.grid(row=1, column=1)

        # Input Last Name
        Label(frame, text="Last name: ").grid(row=2, column=0)
        self.last_name = Entry(frame)
        self.last_name.grid(row=2, column=1)

        # Input password
        Label(frame, text="Password: ").grid(row=3, column=0)
        self.password = Entry(frame, show="*")
        self.password.grid(row=3, column=1)

        # Input Repeat password
        Label(frame, text="Repeat password: ").grid(row=4, column=0)
        self.repeat_password = Entry(frame, show="*")
        self.repeat_password.grid(row=4, column=1)

        # Login button
        ttk.Button(frame, text="Register", command=self.auth_register).grid(
            row=5, columnspan=2, sticky=W + E
        )

        # Output message
        self.message = Label(self, text="", fg="red")
        self.message.grid(row=6, column=0, columnspan=2, sticky=W + E)

    def validation(self):
        return (
            len(self.name.get()) != 0
            and len(self.last_name.get()) != 0
            and len(self.password.get()) != 0
            and self.password.get() == self.repeat_password.get()
        )

    def auth_register(self):
        # Validate input values
        if self.validation():

            # Get input values
            name = self.name.get()
            password = self.password.get()
            last_name = self.last_name.get()
            hashed_password = hashlib.sha256(password.encode()).hexdigest()

            response_data = UserService.create_new_user(
                parameters=(name, last_name, hashed_password)
            )

            # Send output message
            self.message["text"] = response_data

            # Clear all inputs
            self.name.delete(0, END)
            self.last_name.delete(0, END)
            self.password.delete(0, END)
            self.repeat_password.delete(0, END)
        else:
            self.message["text"] = "You need to complete all fields correctly"
