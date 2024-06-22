from tkinter import *


def alert(text):
    alertPopup = Toplevel()
    alertPopup.title = "Agregar personal"

    message = Label(alertPopup, text="", fg="blue", padx=10, pady=10)
    message.grid(row=0, column=0, columnspan=2, sticky=W + E)

    screen_width = alertPopup.winfo_screenwidth()
    screen_height = alertPopup.winfo_screenheight()

    window_width = 400
    window_height = 50

    x_pos = (screen_width - window_width) // 2
    y_pos = (screen_height - window_height) // 2

    alertPopup.geometry(f"{window_width}x{window_height}+{x_pos}+{y_pos}")

    message["text"] = text

    alertPopup.after(3000, alertPopup.destroy)
