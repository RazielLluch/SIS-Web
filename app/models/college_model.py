import json

from ..database.controller import connect_db
from ..models.model import Model


class CollegeModel(Model):
    def __init__(self, college_id=None,
                 name=None,
                 ):
        super().__init__('college')
        self.id = college_id
        self.name = name

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
        }

    def count_all(self):
        try:

            self.db.close()
            self.cur.close()

            self.db, self.cur = connect_db()

            # Assuming `read` method can be used to count rows in the table
            query = f"SELECT COUNT(*) FROM {self.table_name}"
            query_result = self.cur.execute(query)  # `execute` should return the result of the query
            result = self.cur.fetchone()
            return result[0]  # This assumes the count is returned as a tuple like [(count,)]
        except Exception as e:
            print(f"Error counting colleges: {e}")
            return 0
        finally:
            self.db.close()
            self.cur.close()

    def add(self):
        self.create(
            self.table_name,
            self.to_dict()
        )

    def edit(self, basis_id):
        self_dict = self.to_dict()

        print("self_dict: ", self_dict)

        return self.update(
            self.table_name,
            self_dict,
            {"id": basis_id}
        )

    def delete_by_ids(self, course_ids):
        return self.delete(
            self.table_name,
            'id',
            course_ids
        )

    def fetch_all_courses(self):
        # Fetch the data
        result = self.read(self.table_name)

        # Convert the result into a JSON-compatible format
        if result:
            # Assuming result is a list of tuples or dictionaries, convert to list of dictionaries
            if isinstance(result, list):
                # Convert list of tuples to list of dictionaries if needed
                # For example, if the result is [(1, 'John'), (2, 'Jane')], convert it to [{'id': 1, 'name': 'John'}, {'id': 2, 'name': 'Jane'}]
                fields = [desc[0] for desc in self.cur.description]  # Get field names from cursor description
                result = [dict(zip(fields, row)) for row in result]

            # Return as JSON
            return json.dumps(result, default=str)  # Use default=str to handle non-serializable types
        return json.dumps([])  # Return an empty JSON array if no results

    def count_filtered(self, search_term):

        self.db.close()
        self.cur.close()

        # Reconnect to the database
        self.db, self.cur = connect_db()

        query = """
            SELECT COUNT(*) FROM college
            WHERE id LIKE %s
            OR name LIKE %s
        """
        like_term = f"%{search_term}%"
        params = (like_term,) * 2  # 6 columns
        self.cur.execute(query, params)
        return self.cur.fetchone()[0]

    def fetch_paginated(self, page=1, per_page=10):
        try:
            # Close previous connections if any
            self.db.close()
            self.cur.close()

            # Reconnect to the database
            self.db, self.cur = connect_db()

            # Calculate the offset based on page and per_page
            offset = (page - 1) * per_page

            # SQL query to fetch colleges with pagination
            query = f"""
                SELECT * FROM {self.table_name}
                LIMIT {per_page} OFFSET {offset}
            """

            print(f'query: {query}')

            # Execute the query
            self.cur.execute(query)

            # Fetch the results from the cursor
            colleges = self.cur.fetchall()

            print(f'per_page = {per_page}, offset = {offset}')
            print(f'colleges = {colleges}')

            # # Convert rows into a list of Student objects
            # college_objects = [
            #     self.__class__(college_id=college[0], firstname=college[1], lastname=college[2],
            #                    course=college[3], year=college[4], gender=college[5], profile_picture_url=college[6])
            #     for college in colleges
            # ]
            # return college_objects
            return colleges
        except Exception as e:
            print(f"Error fetching paginated colleges: {e}")
            return []
        finally:
            # Close connections
            self.db.close()
            self.cur.close()

    def fetch_filtered_paginated(self, search_term, page, per_page):

        self.db.close()
        self.cur.close()

        # Reconnect to the database
        self.db, self.cur = connect_db()

        offset = (page - 1) * per_page
        query = """
            SELECT * FROM college
            WHERE id LIKE %s
            OR name LIKE %s
            LIMIT %s OFFSET %s
        """
        like_term = f"%{search_term}%"
        params = (like_term,) * 2 + (per_page, offset)
        self.cur.execute(query, params)
        return self.cur.fetchall()