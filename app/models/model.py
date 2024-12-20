from app.database.controller import connect_db


class Model:
    """
    BaseModel: A base class for interacting with the database.
    This class includes basic CRUD functionalities and can be inherited by specific model classes.
    """

    def __init__(self, table_name):
        """
        Initialize the BaseModel with a MySQL instance.
        :param mysql: Flask-MySQLdb MySQL instance.
        """
        self.db, self.cur = connect_db()
        self.table_name = table_name

    def find_by_id(self, id):
        return self.read(self.table_name, conditions={'id': id}, fetch_one=True)

    def fetch_all(self):
        return self.read(self.table_name)

    def execute_query(self, query, params=None, fetch_one=False):
        """
        Execute a raw SQL query.
        :param query: SQL query string.
        :param params: Optional tuple of parameters for the query.
        :param fetch_one: Whether to fetch only one row.
        :return: Query results or None.
        """

        print("Query to execute: ", query)

        self.cur.close()
        self.db.close()

        self.db, self.cur = connect_db()

        try:
            self.cur.execute(query, params or ())
            if query.strip().lower().startswith("select"):
                thing = self.cur.fetchone() if fetch_one else self.cur.fetchall()
                print(thing)
                return thing
            else:
                self.db.commit()
                return self.cur.rowcount
        except Error as e:
            print(f"Database connection failed: {e}")
        finally:
            self.cur.close()

    def create(self, table_name, data):
        """
        Insert a new record into a table.
        :param table_name: Name of the table.
        :param data: Dictionary containing column names and values.
        :return: Last inserted ID.
        """
        data = self.sanitize_data(data)
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['%s'] * len(data))
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        self.db, self.cur = connect_db()
        try:
            self.cur.execute(query, tuple(data.values()))
            self.db.commit()
            result = self.cur.lastrowid
            print("result: ", result)
            return result
        except Exception as e:
            raise e
        finally:
            self.cur.close()

    def read(self, table_name, conditions=None, fields="*", fetch_one=False):
        """
        Fetch records from a table.
        :param table_name: Name of the table.
        :param conditions: Dictionary of column-value pairs for WHERE clause.
        :param fields: Comma-separated string of fields to select.
        :param fetch_one: Whether to fetch only one row.
        :return: Query results or None.
        """
        query = f"SELECT {fields} FROM {table_name}"
        params = None
        if conditions:
            condition_clauses = ' AND '.join([f"{key}=%s" for key in conditions.keys()])
            query += f" WHERE {condition_clauses}"
            params = tuple(conditions.values())
        return self.execute_query(query, params, fetch_one)

    def update(self, table_name, data, conditions):
        """
        Update records in a table.
        :param table_name: Name of the table.
        :param data: Dictionary of columns to update with new values.
        :param conditions: Dictionary of column-value pairs for WHERE clause.
        :return: Number of affected rows.
        """

        self.db, self.cur = connect_db()

        data = self.sanitize_data(data)

        set_clauses = ', '.join([f"{key}=%s" for key in data.keys()])
        condition_clauses = ' AND '.join([f"{key}=%s" for key in conditions.keys()])
        query = f"UPDATE {table_name} SET {set_clauses} WHERE {condition_clauses}"
        params = tuple(data.values()) + tuple(conditions.values())

        try:
            with self.cur as cursor:
                cursor.execute(query, params)
                self.db.commit()
                return True  # Deletion was successful
        except Exception as e:
            self.db.rollback()  # Rollback the transaction in case of error
            return str(e)  # Return the error message

    def delete(self, table_name, column, values):
        """
        Delete records from a table based on a list of values.
        :param table_name: Name of the table.
        :param column: Column name to match values against.
        :param values: List of values for the IN clause.
        :return: True if successful, or the error message if unsuccessful.
        """

        self.db, self.cur = connect_db()

        placeholders = ', '.join(['%s'] * len(values))  # Create placeholders for each value
        query = f"DELETE FROM {table_name} WHERE {column} IN ({placeholders})"
        params = tuple(values)

        try:
            with self.cur as cursor:
                cursor.execute(query, params)
                self.db.commit()
                return True  # Deletion was successful
        except Exception as e:
            self.connection.rollback()  # Rollback the transaction in case of error
            return str(e)  # Return the error message

    @staticmethod
    def sanitize_data(data):
        return {k: (v if v is not None else 'NULL') for k, v in data.items()}
