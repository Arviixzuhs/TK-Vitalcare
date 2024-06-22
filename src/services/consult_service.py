from utils.run_query import run_query


class ConsultService:
    def get_consults():
        query = "SELECT * FROM consult"
        return run_query(query)

    def search_consult(parameters):
        query = "SELECT * FROM consult WHERE id = ? OR reason LIKE ?"
        return run_query(query, parameters)

    def add_consult(parameters):
        query = "INSERT INTO consult (reason, date, doctor_id, patient_id) VALUES (?, ?, ?, ?)"
        run_query(query, parameters)
        return "Consulta agregada correctamente"

    def delete_consult(parameters):
        query = "DELETE FROM consult WHERE id = ?"
        run_query(query, parameters)
        return "Consulta eliminada correctamente"

    def edit_consult(parameters):
        query = "UPDATE consult SET reason = ?, date = ?, doctor_id = ?, patient_id = ? WHERE id = ?"
        run_query(query, parameters)
        return "Consulta actualizada correctamente"
