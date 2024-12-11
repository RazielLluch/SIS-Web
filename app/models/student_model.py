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
        self.table_name = 'student'

    def find_by_id(self, student_id):
        return self.read(self.table_name, conditions={'id': student_id}, fetch_one=True)

    def fetch_all(self):
        return self.read(self.table_name)
