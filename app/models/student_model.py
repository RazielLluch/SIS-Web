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
        super().__init__()
        self.id = student_id
        self.firstname = firstname
        self.lastname = lastname
        self.course = course
        self.year = year
        self.gender = gender
        self.profile_picture_url = profile_picture_url
        self.table_name = 'student'

    def find_by_id(self, student_id):
        return self.read(self.table_name, conditions={'id': student_id}, fetch_one=True)

    def fetch_all(self):
        return self.read(self.table_name)

    def add_student(self):

        self.create(
            self.table_name,
            {
                'id': self.id,  # Example session ID
                'firstname': self.firstname,  # Assuming the user with ID 1 is logged in
                'lastname': self.lastname,
                'course': self.course,  # Example timestamp
                'year': self.year,
                'gender': self.gender,
                'profile_picture_url': self.profile_picture_url
            }
        )

    def delete_by_ids(self, student_ids):
        return self.delete(self.table_name, 'id', student_ids)