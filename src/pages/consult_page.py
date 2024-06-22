from tkinter import *
from tkinter import ttk
from .base_page import Page
from services.consult_service import ConsultService
from utils.alert import alert


class ConsultPage(Page):
    def __init__(self, parent, *args, **kwargs):
        Page.__init__(self, parent, *args, **kwargs)

        # Creando el contenedor Frame
        self.frame = LabelFrame(self, text="Consultas Médicas")
        self.frame.grid(row=0, column=0, columnspan=2, pady=20, padx=20)

        # Tabla para mostrar consultas
        self.tree = ttk.Treeview(self, height=20, columns=(1, 2, 3, 4, 5))
        self.tree.grid(row=2, column=0, columnspan=5)
        self.tree.heading("#0", text="ID", anchor=CENTER)
        self.tree.heading("#1", text="Fecha", anchor=CENTER)
        self.tree.heading("#2", text="Motivo", anchor=CENTER)
        self.tree.heading("#3", text="ID Doctor", anchor=CENTER)
        self.tree.heading("#4", text="ID Paciente", anchor=CENTER)

        # Botones adicionales
        ttk.Button(self, text="Eliminar", command=self.delete_consult).grid(
            row=1, column=0, sticky=W + E
        )

        ttk.Button(self, text="Editar", command=self.edit_consult).grid(
            row=1, column=1, sticky=W + E
        )

        ttk.Button(self, text="Crear", command=self.add_consult).grid(
            row=1, column=2, sticky=W + E
        )

        ttk.Button(self, text="Buscar", command=self.search_consult).grid(
            row=0, column=1, sticky=W + E
        )

        self.search = Entry(self)
        self.search.grid(row=0, column=0, sticky=W + E)

        # Rellenar las filas con consultas existentes
        self.get_consults()

    def get_consults(self):
        # Limpiar la tabla de consultas
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)

        # Obtener las consultas desde el servicio
        result = ConsultService.get_consults()

        # Insertar cada consulta en la tabla
        for row in result:
            self.tree.insert(
                "", 0, text=row[0], values=(row[1], row[2], row[3], row[4])
            )

    def search_consult(self):
        if len(self.search.get()) == 0:
            self.get_consults()
            return alert("El campo de búsqueda no puede estar vacío")

        # Limpiar la tabla de consultas
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)

        # Obtener las consultas desde el servicio
        search_value = self.search.get()
        if search_value.isdigit():
            parameters = (search_value, f"%{search_value}%")
        else:
            parameters = (None, f"%{search_value}%")

        result = ConsultService.search_consult(parameters=parameters)

        if not result:
            return self.get_consults()

        # Insertar cada consulta en la tabla
        for row in result:
            self.tree.insert(
                "", 0, text=row[0], values=(row[1], row[2], row[3], row[4])
            )

    def validation(self):
        return (
            len(self.reason.get()) != 0
            and len(self.date.get()) != 0
            and len(self.doctor_id.get()) != 0
            and len(self.patient_id.get()) != 0
        )

    def add(self):
        if self.validation():
            # Llamar al método estático add_consult de ConsultService
            response_data = ConsultService.add_consult(
                parameters=(
                    self.reason.get(),
                    self.date.get(),
                    self.doctor_id.get(),
                    self.patient_id.get(),
                )
            )
            # Mostrar mensaje de éxito o error
            alert(response_data)

            # Limpiar los campos de entrada
            self.reason.delete(0, END)
            self.date.delete(0, END)
            self.doctor_id.delete(0, END)
            self.patient_id.delete(0, END)

            # Actualizar la tabla de consultas
            self.get_consults()
            self.add_consult_popup.destroy()
            alert("Consulta agregada correctamente")
        else:
            alert("Todos los campos son requeridos")

    def add_consult(self):
        # Campos de entrada para Motivo, Fecha, ID Doctor, ID Paciente
        self.add_consult_popup = Toplevel()
        self.add_consult_popup.title = "Agregar Consulta"

        # Get screen dimensions
        screen_width = self.add_consult_popup.winfo_screenwidth()
        screen_height = self.add_consult_popup.winfo_screenheight()

        # Calculate window dimensions
        window_width = 380  # Adjust as needed
        window_height = 90  # Adjust as needed

        # Calculate window position
        x_pos = (screen_width - window_width) // 2
        y_pos = (screen_height - window_height) // 2

        # Set window geometry and position
        self.add_consult_popup.geometry(
            f"{window_width}x{window_height}+{x_pos}+{y_pos}"
        )

        Label(self.add_consult_popup, text="Motivo: ").grid(row=1, column=0)
        self.reason = Entry(self.add_consult_popup)
        self.reason.focus()
        self.reason.grid(row=1, column=1)

        Label(self.add_consult_popup, text="Fecha: ").grid(row=1, column=2)
        self.date = Entry(self.add_consult_popup)
        self.date.grid(row=1, column=3)

        Label(self.add_consult_popup, text="ID Doctor: ").grid(row=2, column=0)
        self.doctor_id = Entry(self.add_consult_popup)
        self.doctor_id.grid(row=2, column=1)

        Label(self.add_consult_popup, text="ID Paciente: ").grid(row=2, column=2)
        self.patient_id = Entry(self.add_consult_popup)
        self.patient_id.grid(row=2, column=3)

        # Botón para guardar consulta
        ttk.Button(
            self.add_consult_popup, text="Guardar consulta", command=self.add
        ).grid(row=4, columnspan=4, sticky=W + E)

    def delete_consult(self):
        # Obtener la consulta seleccionada en la tabla
        selected_item = self.tree.selection()
        if not selected_item:
            return alert("Por favor seleccione un registro")

        # Obtener el motivo de la consulta seleccionada
        id = self.tree.item(selected_item)["text"]

        # Llamar al método estático delete_consult de ConsultService
        response_data = ConsultService.delete_consult(parameters=(id,))

        # Actualizar la tabla de consultas
        self.get_consults()

        return alert(response_data)

    def edit_consult(self):
        # Obtener la consulta seleccionada en la tabla
        selected_item = self.tree.selection()
        if not selected_item:
            return alert("Por favor, seleccione un registro")

        # Obtener los datos de la consulta seleccionada
        consult_id = self.tree.item(selected_item)["text"]
        old_date = self.tree.item(selected_item)["values"][0]
        old_reason = self.tree.item(selected_item)["values"][1]
        old_doctor_id = self.tree.item(selected_item)["values"][2]
        old_patient_id = self.tree.item(selected_item)["values"][3]

        # Crear una ventana emergente para editar la consulta
        self.edit_wind = Toplevel()
        self.edit_wind.title("Editar Consulta")

        # Campos de entrada para editar la consulta
        Label(self.edit_wind, text="Nuevo motivo:").grid(row=1, column=1)
        new_reason = Entry(self.edit_wind)
        new_reason.grid(row=1, column=2)
        new_reason.insert(0, old_reason)

        Label(self.edit_wind, text="Nueva fecha:").grid(row=2, column=1)
        new_date = Entry(self.edit_wind)
        new_date.grid(row=2, column=2)
        new_date.insert(0, old_date)

        Label(self.edit_wind, text="Nuevo ID Doctor:").grid(row=3, column=1)
        new_doctor_id = Entry(self.edit_wind)
        new_doctor_id.grid(row=3, column=2)
        new_doctor_id.insert(0, old_doctor_id)

        Label(self.edit_wind, text="Nuevo ID Paciente:").grid(row=4, column=1)
        new_patient_id = Entry(self.edit_wind)
        new_patient_id.grid(row=4, column=2)
        new_patient_id.insert(0, old_patient_id)

        # Botón para actualizar los datos de la consulta
        Button(
            self.edit_wind,
            text="Actualizar",
            command=lambda: self.edit_records(
                new_reason.get(),
                new_date.get(),
                new_doctor_id.get(),
                new_patient_id.get(),
                consult_id,
            ),
        ).grid(row=5, column=2, sticky=W)

    def edit_records(
        self, new_reason, new_date, new_doctor_id, new_patient_id, consult_id
    ):
        # Llamar al método estático edit_consult de ConsultService
        response_data = ConsultService.edit_consult(
            parameters=(
                new_reason,
                new_date,
                new_doctor_id,
                new_patient_id,
                consult_id,
            )
        )
        self.edit_wind.destroy()  # Cerrar la ventana de edición

        self.get_consults()  # Actualizar la tabla de consultas

        return alert(response_data)
