from tkinter import *
from tkinter import ttk
from .base_page import Page
from services.patient_service import PatientService
from utils.alert import alert


class PatientPage(Page):
    def __init__(self, parent, *args, **kwargs):
        Page.__init__(self, parent, *args, **kwargs)

        # Creando el contenedor Frame
        self.frame = LabelFrame(self, text="Pacientes")
        self.frame.grid(row=0, column=0, columnspan=2, pady=20, padx=20)

        # Tabla para mostrar pacientes
        self.tree = ttk.Treeview(self, height=20, columns=(1, 2, 3, 4, 5, 6))
        self.tree.grid(row=2, column=0, columnspan=5)
        self.tree.heading("#0", text="ID", anchor=CENTER)
        self.tree.heading("#1", text="Nombre", anchor=CENTER)
        self.tree.heading("#2", text="Apellido", anchor=CENTER)
        self.tree.heading("#3", text="Cédula", anchor=CENTER)
        self.tree.heading("#4", text="Teléfono", anchor=CENTER)
        self.tree.heading("#5", text="Dirección", anchor=CENTER)
        self.tree.heading("#6", text="Diagnóstico", anchor=CENTER)

        # Botones adicionales
        ttk.Button(self, text="Eliminar", command=self.delete_patient).grid(
            row=1, column=0, sticky=W + E
        )

        ttk.Button(self, text="Editar", command=self.edit_patient).grid(
            row=1, column=1, sticky=W + E
        )

        ttk.Button(self, text="Crear", command=self.add_patient).grid(
            row=1, column=2, sticky=W + E
        )

        ttk.Button(self, text="Buscar", command=self.search_patient).grid(
            row=0, column=1, sticky=W + E
        )

        self.search = Entry(self)
        self.search.grid(row=0, column=0, sticky=W + E)

        # Rellenar las filas con pacientes existentes
        self.get_patients()

    def get_patients(self):
        # Limpiar la tabla de pacientes
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)

        # Obtener los pacientes desde el servicio
        result = PatientService.get_patients()

        # Insertar cada paciente en la tabla
        for row in result:
            self.tree.insert(
                "",
                0,
                text=row[0],
                values=(row[1], row[2], row[3], row[4], row[5], row[6]),
            )

    def search_patient(self):
        if len(self.search.get()) == 0:
            self.get_patients()
            return alert("El campo de búsqueda no puede estar vacío")

        # Limpiar la tabla de pacientes
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)

        # Obtener las consultas desde el servicio
        search_value = self.search.get()
        if search_value.isdigit():
            parameters = (search_value, f"%{search_value}%")
        else:
            parameters = (None, f"%{search_value}%")

        result = PatientService.search_patient(parameters=parameters)

        if not result:
            return self.get_patients()

        # Insertar cada paciente en la tabla
        for row in result:
            self.tree.insert(
                "",
                0,
                text=row[0],
                values=(row[1], row[2], row[3], row[4], row[5], row[6]),
            )

    def validation(self):
        return (
            len(self.nombre.get()) != 0
            and len(self.apellido.get()) != 0
            and len(self.cedula.get()) != 0
            and len(self.telefono.get()) != 0
            and len(self.direccion.get()) != 0
            and len(self.diagnostico.get()) != 0
        )

    def add(self):
        if self.validation():
            # Llamar al método estático add_patient de PatientService
            response_data = PatientService.add_patient(
                parameters=(
                    self.nombre.get(),
                    self.apellido.get(),
                    self.cedula.get(),
                    self.telefono.get(),
                    self.direccion.get(),
                    self.diagnostico.get(),
                )
            )
            # Mostrar mensaje de éxito o error
            alert(response_data)

            # Limpiar los campos de entrada
            self.nombre.delete(0, END)
            self.apellido.delete(0, END)
            self.cedula.delete(0, END)
            self.telefono.delete(0, END)
            self.direccion.delete(0, END)
            self.diagnostico.delete(0, END)

            # Actualizar la tabla de pacientes
            self.get_patients()
            self.add_patient_popup.destroy()
            alert("Paciente agregado correctamente")
        else:
            alert("Todos los campos son requeridos")

    def add_patient(self):
        # Campos de entrada para Nombre, Apellido, Cédula, Teléfono, Dirección y Diagnóstico
        self.add_patient_popup = Toplevel()
        self.add_patient_popup.title = "Agregar paciente"

        # Get screen dimensions
        screen_width = self.add_patient_popup.winfo_screenwidth()
        screen_height = self.add_patient_popup.winfo_screenheight()

        # Calculate window dimensions
        window_width = 480  # Adjust as needed
        window_height = 110  # Adjust as needed

        # Calculate window position
        x_pos = (screen_width - window_width) // 2
        y_pos = (screen_height - window_height) // 2

        # Set window geometry and position
        self.add_patient_popup.geometry(
            f"{window_width}x{window_height}+{x_pos}+{y_pos}"
        )

        Label(self.add_patient_popup, text="Nombre: ").grid(row=1, column=0)
        self.nombre = Entry(self.add_patient_popup)
        self.nombre.focus()
        self.nombre.grid(row=1, column=1)

        Label(self.add_patient_popup, text="Apellido: ").grid(row=1, column=2)
        self.apellido = Entry(self.add_patient_popup)
        self.apellido.grid(row=1, column=3)

        Label(self.add_patient_popup, text="Cédula: ").grid(row=2, column=0)
        self.cedula = Entry(self.add_patient_popup)
        self.cedula.grid(row=2, column=1)

        Label(self.add_patient_popup, text="Teléfono: ").grid(row=2, column=2)
        self.telefono = Entry(self.add_patient_popup)
        self.telefono.grid(row=2, column=3)

        Label(self.add_patient_popup, text="Dirección: ").grid(row=3, column=0)
        self.direccion = Entry(self.add_patient_popup)
        self.direccion.grid(row=3, column=1)

        Label(self.add_patient_popup, text="Diagnóstico: ").grid(row=3, column=2)
        self.diagnostico = Entry(self.add_patient_popup)
        self.diagnostico.grid(row=3, column=3)

        # Botón para guardar paciente
        ttk.Button(
            self.add_patient_popup, text="Guardar paciente", command=self.add
        ).grid(row=4, columnspan=4, sticky=W + E)

    def delete_patient(self):
        # Obtener el ID del paciente seleccionado en la tabla
        selected_item = self.tree.selection()
        if not selected_item:
            return alert("Por favor seleccione un registro")

        # Obtener el ID del paciente seleccionado
        patient_id = self.tree.item(selected_item)["text"]

        # Llamar al método estático delete_patient de PatientService
        response_data = PatientService.delete_patient(parameters=(patient_id,))

        # Actualizar la tabla de pacientes
        self.get_patients()

        return alert(response_data)

    def edit_patient(self):
        # Obtener el ID del paciente seleccionado en la tabla
        selected_item = self.tree.selection()
        if not selected_item:
            return alert("Por favor seleccione un registro")

        # Obtener los datos del paciente seleccionado
        patient_id = self.tree.item(selected_item)["text"]
        paciente = self.tree.item(selected_item)["values"]

        # Crear ventana para editar paciente
        self.edit_patient_popup = Toplevel()
        self.edit_patient_popup.title = "Editar paciente"

        # Get screen dimensions
        screen_width = self.edit_patient_popup.winfo_screenwidth()
        screen_height = self.edit_patient_popup.winfo_screenheight()

        # Calculate window dimensions
        window_width = 480  # Adjust as needed
        window_height = 110  # Adjust as needed

        # Calculate window position
        x_pos = (screen_width - window_width) // 2
        y_pos = (screen_height - window_height) // 2

        # Set window geometry and position
        self.edit_patient_popup.geometry(
            f"{window_width}x{window_height}+{x_pos}+{y_pos}"
        )

        Label(self.edit_patient_popup, text="Nombre: ").grid(row=1, column=0)
        self.nombre = Entry(self.edit_patient_popup)
        self.nombre.insert(0, paciente[0])
        self.nombre.grid(row=1, column=1)

        Label(self.edit_patient_popup, text="Apellido: ").grid(row=1, column=2)
        self.apellido = Entry(self.edit_patient_popup)
        self.apellido.insert(0, paciente[1])
        self.apellido.grid(row=1, column=3)

        Label(self.edit_patient_popup, text="Cédula: ").grid(row=2, column=0)
        self.cedula = Entry(self.edit_patient_popup)
        self.cedula.insert(0, paciente[2])
        self.cedula.grid(row=2, column=1)

        Label(self.edit_patient_popup, text="Teléfono: ").grid(row=2, column=2)
        self.telefono = Entry(self.edit_patient_popup)
        self.telefono.insert(0, paciente[3])
        self.telefono.grid(row=2, column=3)

        Label(self.edit_patient_popup, text="Dirección: ").grid(row=3, column=0)
        self.direccion = Entry(self.edit_patient_popup)
        self.direccion.insert(0, paciente[4])
        self.direccion.grid(row=3, column=1)

        Label(self.edit_patient_popup, text="Diagnóstico: ").grid(row=3, column=2)
        self.diagnostico = Entry(self.edit_patient_popup)
        self.diagnostico.insert(0, paciente[5])
        self.diagnostico.grid(row=3, column=3)

        # Botón para guardar cambios
        ttk.Button(
            self.edit_patient_popup,
            text="Guardar cambios",
            command=lambda: self.update_patient(patient_id),
        ).grid(row=4, columnspan=4, sticky=W + E)

    def update_patient(self, patient_id):
        if self.validation():
            # Llamar al método estático edit_patient de PatientService
            response_data = PatientService.edit_patient(
                parameters=(
                    self.nombre.get(),
                    self.apellido.get(),
                    self.cedula.get(),
                    self.telefono.get(),
                    self.direccion.get(),
                    self.diagnostico.get(),
                    patient_id,
                )
            )
            # Mostrar mensaje de éxito o error
            alert(response_data)

            # Actualizar la tabla de pacientes
            self.get_patients()
            self.edit_patient_popup.destroy()
            alert("Paciente actualizado correctamente")
        else:
            alert("Todos los campos son requeridos")
