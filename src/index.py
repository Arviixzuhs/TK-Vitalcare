from tkinter import Tk
from tkinter import ttk
from pages.login_page import LoginPage
from pages.consult_page import ConsultPage
from pages.register_page import RegisterPage
from pages.profile_page import ProfilePage
from db.db_createTables import dbCreateTables
from pages.patient_page import PatientPage
from pages.clinical_staff_page import ClinicalStaffPage


# Default auth pages
class AuthApplication:
    def __init__(self, root):
        self.root = root
        self.root.title("Vitalcare - Inicia sesión o registrate")

        # Create inital notebook
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(pady=10, expand=True)

        # Initial login page
        self.login_page = LoginPage(self.notebook, self.login_success)
        self.notebook.add(self.login_page, text="Login")

        # Initial register page
        self.register_page = RegisterPage(self.notebook)
        self.notebook.add(self.register_page, text="Registro")

    # Login success callback
    def login_success(self, user):
        self.root.destroy()
        main_window = Tk()
        MainApplication(main_window, user)
        main_window.mainloop()


class MainApplication:
    def __init__(self, root, user):
        self.root = root
        self.root.title("Vitalcare")

        # Create inital notebook
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True)

        # Patient page
        self.patient_page = PatientPage(self.notebook)
        self.notebook.add(self.patient_page, text="Pacientes")

        # Staff page
        self.staff_page = ClinicalStaffPage(self.notebook)
        self.notebook.add(self.staff_page, text="Personal")

        # Consult page
        self.consult_page = ConsultPage(self.notebook)
        self.notebook.add(self.consult_page, text="Consultas")

        # Profile page
        self.profile_page = ProfilePage(self.notebook, user)
        self.notebook.add(self.profile_page, text="Profile")


if __name__ == "__main__":
    dbCreateTables()
    window = Tk()

    window_width = 380
    window_height = 240

    x_window = window.winfo_screenwidth() // 2 - window_width // 2
    y_window = window.winfo_screenheight() // 2 - window_height // 2

    posicion = (
        str(window_width)
        + "x"
        + str(window_height)
        + "+"
        + str(x_window)
        + "+"
        + str(y_window)
    )
    window.geometry(posicion)

    app = AuthApplication(window)
    window.mainloop()
