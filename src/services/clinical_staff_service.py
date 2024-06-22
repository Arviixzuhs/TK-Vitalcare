from utils.run_query import run_query


class ClinicalStaffService:
    def get_clinical_staff():
        query = "SELECT * FROM clinicalstaff"
        result = run_query(query)
        return result

    def add_clinical_staff(parameters):
        query = "INSERT INTO clinicalstaff VALUES(NULL, ?, ?, ?, ?, ?, ?)"
        run_query(query, parameters)
        return "Trabajador agregado exitosamente"

    def delete_clinical_staff(parameters):
        query = "DELETE FROM clinicalstaff WHERE id = ?"
        run_query(query, parameters)
        return "Registro eliminado exitosamente"

    def edit_clinical_staff(parameters):
        query = "UPDATE clinicalstaff SET name = ?, last_name = ?, dni = ?, phone = ?, address = ?, position = ? WHERE id = ?"
        run_query(query, parameters)
        return "Registro actualizado correctamente"

    def search_clinical_staff(parameters):
        query = "SELECT * FROM clinicalstaff WHERE id = ? OR name LIKE ?"
        result = run_query(query, parameters)
        return result
