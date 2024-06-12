from utils.run_query import run_query


class UserService:
    def find_user_by_id(parameters):
        query = "SELECT * FROM users WHERE id = ?"
        result = run_query(query, parameters).fetchone()
        return result

    def get_login(parameters):
        query = "SELECT * FROM users WHERE name = ? AND password = ?"
        result = run_query(query, parameters).fetchone()
        return result

    def create_new_user(parameters):
        query = "INSERT INTO users (name, last_name, password) VALUES (?, ?, ?)"
        run_query(query, parameters).fetchone()
        return "User has been registered"

    def update_profile(parameters):
        query = "UPDATE users SET name = ?, last_name = ? WHERE id = ?"
        run_query(query, parameters).fetchone()
        return "Profile updated successfully"

    def update_password(parameters):
        query = "UPDATE users SET password = ? WHERE id = ?"
        run_query(query, parameters).fetchone()
        return "Password updated successfully"
