import hashlib
from tkinter import Label, Entry, LabelFrame, W, E, Button, END
from .base_page import Page
from services.user_service import UserService


class ProfilePage(Page):
    def __init__(self, parent, user, *args, **kwargs):
        Page.__init__(self, parent, *args, **kwargs)

        self.user = user
        self.user_id = user[0]

        # User profile tab
        self.frame = LabelFrame(self, text="User Profile")
        self.frame.grid(row=0, column=0, columnspan=2, pady=20, padx=20)

        # Input Name
        Label(self.frame, text="Name: ").grid(row=1, column=0, sticky="w")
        self.name_entry = Entry(self.frame)
        self.name_entry.grid(row=1, column=1, sticky="w")
        self.name_entry.insert(0, user[1])

        # Input Last Name
        Label(self.frame, text="Last Name: ").grid(row=2, column=0, sticky="w")
        self.last_name_entry = Entry(self.frame)
        self.last_name_entry.grid(row=2, column=1, sticky="w")
        self.last_name_entry.insert(0, user[2])

        # Update Profile Button
        self.update_button = Button(
            self.frame, text="Update Profile", command=self.update_profile
        )
        self.update_button.grid(row=5, columnspan=2, sticky=W + E)

        # Output message change info profile
        self.message_1 = Label(self.frame, text="", fg="red")
        self.message_1.grid(row=4, columnspan=2, sticky=W + E)

        # User change password tab
        self.change_password_frame = LabelFrame(self, text="Change password")
        self.change_password_frame.grid(row=3, column=0, columnspan=2, pady=20, padx=20)

        # Input Password
        Label(self.change_password_frame, text="Password: ").grid(
            row=3, column=0, sticky="w"
        )
        self.password_entry = Entry(self.change_password_frame, show="*")
        self.password_entry.grid(row=3, column=1, sticky="w")

        # Change password button
        self.update_button = Button(
            self.change_password_frame,
            text="Change password",
            command=self.change_password,
        )
        self.update_button.grid(row=5, columnspan=2, sticky=W + E)

        # Output message change password
        self.message_2 = Label(self.change_password_frame, text="", fg="red")
        self.message_2.grid(row=4, columnspan=2, sticky=W + E)

    def update_profile(self):
        # Get input values
        name = self.name_entry.get()
        last_name = self.last_name_entry.get()

        if not name or not last_name:
            return self.message_1.config(text="Name, Last Name cannot be empty")

        response_data = UserService.update_profile(
            parameters=(name, last_name, self.user_id)
        )

        self.message_1.config(text=response_data)

    def change_password(self):
        password = self.password_entry.get()
        if not password:
            return self.message_2.config(text="Password cannot be empty")

        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        response_data = UserService.update_password(
            parameters=(hashed_password, self.user_id)
        )
        self.message_2.config(text=response_data)
