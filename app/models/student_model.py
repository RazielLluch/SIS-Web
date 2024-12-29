from ..database.controller import connect_db
from ..models.model import Model


class StudentModel(Model):

    def __init__(self, student_id=None,
                 firstname=None,
                 lastname=None,
                 course=None,
                 year=None,
                 gender=None,
                 profile_picture_url=None
                 ):
        super().__init__('student')
        self.id = student_id
        self.firstname = firstname
        self.lastname = lastname
        self.course = course
        self.year = year
        self.gender = gender
        self.profile_picture_url = profile_picture_url

    def to_dict(self):
        return {
            'id': self.id,
            'firstname': self.firstname,
            'lastname': self.lastname,
            'course': self.course,
            'year': self.year,
            'gender': self.gender,
            'profile_picture_url': self.profile_picture_url,
        }

    # def find_by_id(self, student_id):
    #     return self.read(self.table_name, conditions={'id': student_id}, fetch_one=True)
    #
    # def fetch_all(self):
    #     return self.read(self.table_name)

    # Method to count all students in the database
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
            print(f"Error counting students: {e}")
            return 0
        finally:
            self.db.close()
            self.cur.close()

    # Method to fetch students with pagination
    def fetch_paginated(self, page=1, per_page=10):
        try:
            # Calculate the offset based on page and per_page
            offset = (page - 1) * per_page

            # SQL query to fetch students with pagination
            query = f"""
                SELECT * FROM {self.table_name}
                LIMIT {per_page} OFFSET {offset}
            """
            students_query = self.cur.execute(query)  # Execute the query to fetch paginated results

            students = students_query.fetchall()

            print(f'per_page = {per_page}, offset = {offset}')
            print(f'students = {students}')

            # Convert rows into a list of Student objects
            student_objects = [self.__class__(**student) for student in students]
            return student_objects
        except Exception as e:
            print(f"Error fetching paginated students: {e}")
            return []

    def add(self):
        try:
            self.create(
                self.table_name,
                self.to_dict()
            )
        except Exception as e:
            raise e

    def edit(self, basis_id):
        self_dict = self.to_dict()
        if self.profile_picture_url is None:
            self_dict.pop('profile_picture_url')

        print(self_dict)

        return self.update(
            self.table_name,
            self_dict,
            {"id": basis_id}
        )

    def delete_by_ids(self, student_ids):
        return self.delete(
            self.table_name,
            'id',
            student_ids
        )

    # def is_valid_id
