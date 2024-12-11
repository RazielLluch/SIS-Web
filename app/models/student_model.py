from ..models.model import Model


class StudentModel(Model):
    def __init__(self):
        super().__init__()
        self.table_name = 'student'

    def find_by_id(self, student_id):
        return self.read(self.table_name, conditions={'id': student_id}, fetch_one=True)

    def fetch_all(self):
        return self.read(self.table_name)
