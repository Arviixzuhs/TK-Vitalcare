from tkinter import Label, Entry, LabelFrame, W, E, Button, END
from .base_page import Page
from utils.run_query import run_query


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

        # Input Password
        Label(self.frame, text="Password: ").grid(row=3, column=0, sticky="w")
        self.password_entry = Entry(self.frame, show="*")
        self.password_entry.grid(row=3, column=1, sticky="w")

        # Update Profile
        self.update_button = Button(
            self.frame, text="Update Profile", command=self.update_profile
        )
        self.update_button.grid(row=4, columnspan=2, sticky=W + E)

        # Output message
        self.message = Label(self.frame, text="", fg="red")
        self.message.grid(row=5, columnspan=2, sticky=W + E)

    def update_profile(self):
        # Get input values
        name = self.name_entry.get()
        last_name = self.last_name_entry.get()
        password = self.password_entry.get()

        if not name or not last_name:
            self.message.config(text="Name and Last Name cannot be empty")
            return

        parameters = [name, last_name]
        if password:
            import hashlib

            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            parameters.append(hashed_password)
            query = (
                "UPDATE users SET name = ?, last_name = ?, password = ? WHERE id = ?"
            )
        else:
            query = "UPDATE users SET name = ?, last_name = ? WHERE id = ?"

        parameters.append(self.user_id)
        run_query(query, parameters)

        self.message.config(text="Profile updated successfully")
