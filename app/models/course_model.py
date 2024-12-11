from ..models.model import Model


class CourseModel(Model):
    def __init__(self, course_id=None,
                 name=None,
                 college=None
                 ):
        super().__init__()
        self.table_name = 'course'
        self.course_id = course_id
        self.name = name
        self.college = college

    def find_by_id(self):
        return self.read(self.table_name, conditions={'id': self.course_id}, fetch_one=True)

    def fetch_all(self):
        return self.read(self.table_name)
