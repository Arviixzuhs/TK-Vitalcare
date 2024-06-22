# services/patient_service.py
from utils.run_query import run_query


class PatientService:
    def get_patients():
        query = "SELECT * FROM patient"
        return run_query(query)

    def search_patient(parameters):
        query = "SELECT * FROM patient WHERE id = ? OR name LIKE ?"
        return run_query(query, parameters)

    def add_patient(parameters):
        query = "INSERT INTO patient (name, last_name, dni, phone, address, diagnosis) VALUES (?, ?, ?, ?, ?, ?)"
        run_query(query, parameters)
        return "Paciente agregado correctamente"

    def delete_patient(parameters):
        query = "DELETE FROM patient WHERE id = ?"
        run_query(query, parameters)
        return "Paciente eliminado correctamente"

    def edit_patient(parameters):
        query = "UPDATE patient SET name = ?, last_name = ?, dni = ?, phone = ?, address = ?, diagnosis = ? WHERE id = ?"
        run_query(query, parameters)
        return "Paciente actualizado correctamente"
