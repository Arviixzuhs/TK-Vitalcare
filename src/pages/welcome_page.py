from tkinter import Label
from .base_page import Page


class WelcomePage(Page):
    def __init__(self, parent, *args, **kwargs):
        Page.__init__(self, parent, *args, **kwargs)
        Label(self, text="Welcome to the Application!").pack(pady=20)
        Label(self, text="Use the tabs above to navigate.").pack(pady=10)
