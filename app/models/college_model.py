from ..models.model import Model


class CollegeModel(Model):
    def __init__(self, college_id=None,
                 name=None,
                 ):
        super().__init__()
        self.table_name = 'college'
        self.college_id = college_id
        self.name = name

    def find_by_id(self):
        return self.read(self.table_name, conditions={'id': self.college_id}, fetch_one=True)

    def fetch_all(self):
        return self.read(self.table_name)
