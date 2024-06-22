from tkinter import *
from tkinter import ttk
from .base_page import Page
from services.clinical_staff_service import ClinicalStaffService
from utils.alert import alert


class ClinicalStaffPage(Page):
    def __init__(self, parent, *args, **kwargs):
        Page.__init__(self, parent, *args, **kwargs)

        # Creando el contenedor Frame
        self.frame = LabelFrame(self, text="User Profile")
        self.frame.grid(row=0, column=0, columnspan=2, pady=20, padx=20)

        # Tabla para mostrar personal
        self.tree = ttk.Treeview(self, height=20, columns=(1, 2, 3, 4, 5, 6))
        self.tree.grid(row=2, column=0, columnspan=5)
        self.tree.heading("#0", text="ID", anchor=CENTER)
        self.tree.heading("#1", text="Nombre", anchor=CENTER)
        self.tree.heading("#2", text="Apellido", anchor=CENTER)
        self.tree.heading("#3", text="Cédula", anchor=CENTER)
        self.tree.heading("#4", text="Teléfono", anchor=CENTER)
        self.tree.heading("#5", text="Dirección", anchor=CENTER)
        self.tree.heading("#6", text="Cargo", anchor=CENTER)

        # Botones adicionales
        ttk.Button(self, text="Eliminar", command=self.delete_clinical_staff).grid(
            row=1, column=0, sticky=W + E
        )

        ttk.Button(self, text="Editar", command=self.edit_clinical_staff).grid(
            row=1, column=1, sticky=W + E
        )

        ttk.Button(self, text="Crear", command=self.add_clinical_staff).grid(
            row=1, column=2, sticky=W + E
        )

        ttk.Button(self, text="Buscar", command=self.search_clinical_staff).grid(
            row=0, column=1, sticky=W + E
        )

        self.search = Entry(self)
        self.search.grid(row=0, column=0, sticky=W + E)

        # Rellenar las filas con personal existentes
        self.get_clinical_staff()

    def get_clinical_staff(self):
        # Limpiar la tabla de personal
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)

        # Obtener el personal desde el servicio
        result = ClinicalStaffService.get_clinical_staff()

        # Insertar cada personal en la tabla
        for row in result:
            self.tree.insert(
                "",
                0,
                text=row[0],
                values=(row[1], row[2], row[3], row[4], row[5], row[6]),
            )

    def search_clinical_staff(self):
        if len(self.search.get()) == 0:
            self.get_clinical_staff()
            return alert("El campo de búsqueda no puede estar vacío")

        # Limpiar la tabla de personal
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)

        # Obtener las consultas desde el servicio
        search_value = self.search.get()
        if search_value.isdigit():
            parameters = (search_value, f"%{search_value}%")
        else:
            parameters = (None, f"%{search_value}%")

        result = ClinicalStaffService.search_clinical_staff(parameters=parameters)

        if not result:
            return self.get_clinical_staff()

        # Insertar cada personal en la tabla
        for row in result:
            self.tree.insert(
                "",
                0,
                text=row[0],
                values=(row[1], row[2], row[3], row[4], row[5], row[6]),
            )

    def validation(self):
        return (
            len(self.name.get()) != 0
            and len(self.last_name.get()) != 0
            and len(self.cedula.get()) != 0
            and len(self.phone.get()) != 0
            and len(self.address.get()) != 0
            and len(self.cargo.get()) != 0
        )

    def a(self):
        if self.validation():
            # Llamar al método estático add_clinical_staff de ClinicalStaffService
            response_data = ClinicalStaffService.add_clinical_staff(
                parameters=(
                    self.name.get(),
                    self.last_name.get(),
                    self.cedula.get(),
                    self.phone.get(),
                    self.address.get(),
                    self.cargo.get(),
                )
            )
            # Mostrar mensaje de éxito o error
            alert(response_data)

            # Limpiar los campos de entrada
            self.name.delete(0, END)
            self.last_name.delete(0, END)
            self.cedula.delete(0, END)
            self.phone.delete(0, END)
            self.address.delete(0, END)
            self.cargo.delete(0, END)

            # Actualizar la tabla de personal
            self.get_clinical_staff()
            self.add_staff_popup.destroy()
            alert("Usuario agregado correctamente")
        else:
            alert("Todos los campos son requeridos")

    def add_clinical_staff(self):
        # Campos de entrada para Nombre, Apellido, Cédula, Teléfono, Dirección y cargo
        self.add_staff_popup = Toplevel()
        self.add_staff_popup.title = "Agregar personal"

        # Get screen dimensions
        screen_width = self.add_staff_popup.winfo_screenwidth()
        screen_height = self.add_staff_popup.winfo_screenheight()

        # Calculate window dimensions
        window_width = 380  # Adjust as needed
        window_height = 90  # Adjust as needed

        # Calculate window position
        x_pos = (screen_width - window_width) // 2
        y_pos = (screen_height - window_height) // 2

        # Set window geometry and position
        self.add_staff_popup.geometry(f"{window_width}x{window_height}+{x_pos}+{y_pos}")

        Label(self.add_staff_popup, text="Nombre: ").grid(row=1, column=0)
        self.name = Entry(self.add_staff_popup)
        self.name.focus()
        self.name.grid(row=1, column=1)

        Label(self.add_staff_popup, text="Apellido: ").grid(row=1, column=2)
        self.last_name = Entry(self.add_staff_popup)
        self.last_name.grid(row=1, column=3)

        Label(self.add_staff_popup, text="Cédula: ").grid(row=2, column=0)
        self.cedula = Entry(self.add_staff_popup)
        self.cedula.grid(row=2, column=1)

        Label(self.add_staff_popup, text="Teléfono: ").grid(row=2, column=2)
        self.phone = Entry(self.add_staff_popup)
        self.phone.grid(row=2, column=3)

        Label(self.add_staff_popup, text="Dirección: ").grid(row=3, column=0)
        self.address = Entry(self.add_staff_popup)
        self.address.grid(row=3, column=1)

        Label(self.add_staff_popup, text="Cargo: ").grid(row=3, column=2)
        self.cargo = Entry(self.add_staff_popup)
        self.cargo.grid(row=3, column=3)

        # Botón para guardar personal
        ttk.Button(
            self.add_staff_popup, text="Guardar trabajador", command=self.a
        ).grid(row=4, columnspan=4, sticky=W + E)

    def delete_clinical_staff(self):
        # Obtener el nombre del personal seleccionado en la tabla
        selected_item = self.tree.selection()
        if not selected_item:
            return alert("Por favor seleccione un registro")

        # Obtener el nombre del personal seleccionado
        id = self.tree.item(selected_item)["text"]

        # Llamar al método estático delete_clinical_staff de Clinical_Staff_Service
        response_data = ClinicalStaffService.delete_clinical_staff(parameters=(id,))

        # Actualizar la tabla del personal
        self.get_clinical_staff()

        return alert(response_data)

    def edit_clinical_staff(self):
        # Obtener el trabajador seleccionado en la tabla
        selected_item = self.tree.selection()
        if not selected_item:
            return alert("Por favor, seleccione un registro")

        # Obtener los datos del trabajador seleccionado
        staff_id = self.tree.item(selected_item)["text"]
        print(staff_id)
        name = self.tree.item(selected_item)["values"][0]
        print(name)
        old_last_name = self.tree.item(selected_item)["values"][1]
        old_cedula = self.tree.item(selected_item)["values"][2]
        old_phone = self.tree.item(selected_item)["values"][3]
        old_address = self.tree.item(selected_item)["values"][4]
        old_cargo = self.tree.item(selected_item)["values"][5]

        # Crear una ventana emergente para editar el trabajador
        self.edit_wind = Toplevel()
        self.edit_wind.title("Editar Paciente")

        # Campos de entrada para editar el trabajador
        Label(self.edit_wind, text="Nuevo nombre:").grid(row=1, column=1)
        new_name = Entry(self.edit_wind)
        new_name.grid(row=1, column=2)
        new_name.insert(0, name)

        Label(self.edit_wind, text="Nuevo apellido:").grid(row=2, column=1)
        new_last_name = Entry(self.edit_wind)
        new_last_name.grid(row=2, column=2)
        new_last_name.insert(0, old_last_name)

        Label(self.edit_wind, text="Nueva cédula:").grid(row=3, column=1)
        new_cedula = Entry(self.edit_wind)
        new_cedula.grid(row=3, column=2)
        new_cedula.insert(0, old_cedula)

        Label(self.edit_wind, text="Nuevo teléfono:").grid(row=4, column=1)
        new_phone = Entry(self.edit_wind)
        new_phone.grid(row=4, column=2)
        new_phone.insert(0, old_phone)

        Label(self.edit_wind, text="Nueva dirección:").grid(row=5, column=1)
        new_address = Entry(self.edit_wind)
        new_address.grid(row=5, column=2)
        new_address.insert(0, old_address)

        Label(self.edit_wind, text="Nuevo cargo:").grid(row=6, column=1)
        new_cargo = Entry(self.edit_wind)
        new_cargo.grid(row=6, column=2)
        new_cargo.insert(0, old_cargo)

        # Botón para actualizar los datos del trabajador
        Button(
            self.edit_wind,
            text="Actualizar",
            command=lambda: self.edit_records(
                new_name.get(),
                new_last_name.get(),
                new_cedula.get(),
                new_phone.get(),
                new_address.get(),
                new_cargo.get(),
                staff_id,
            ),
        ).grid(row=7, column=2, sticky=W)

    def edit_records(
        self,
        new_name,
        new_last_name,
        new_cedula,
        new_phone,
        new_address,
        new_cargo,
        staff_id,
    ):
        # Llamar al método estático edit_clinical_staff de Clinical_Staff_Service
        response_data = ClinicalStaffService.edit_clinical_staff(
            parameters=(
                new_name,
                new_last_name,
                new_cedula,
                new_phone,
                new_address,
                new_cargo,
                staff_id,
            )
        )
        self.edit_wind.destroy()  # Cerrar la ventana de edición

        self.get_clinical_staff()  # Actualizar la tabla de pacientes

        return alert(response_data)
