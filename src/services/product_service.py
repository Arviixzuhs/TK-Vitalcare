from utils.run_query import run_query


class ProductService:
    def get_products():
        query = "SELECT * FROM product ORDER BY name DESC"
        result = run_query(query)
        return result

    def add_product(parameters):
        query = "INSERT INTO product VALUES(NULL, ?, ?)"
        run_query(query, parameters)
        return "Product added successfully"

    def delete_product(parameters):
        query = "DELETE FROM product WHERE name = ?"
        run_query(query, parameters)
        return "Record deleted Successfully"

    def edit_product(parameters):
        query = "UPDATE product SET name = ?, price = ? WHERE name = ? AND price = ?"
        run_query(query, parameters)
        return "Record updated successfully"
