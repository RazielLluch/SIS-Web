from ..models.model import Model


class CourseModel(Model):
    def __init__(self, course_id=None,
                 name=None,
                 college=None
                 ):
        super().__init__('course')
        self.id = course_id
        self.name = name
        self.college = college

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'college': self.college,
        }

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

    @staticmethod
    def delete_by_ids(course_ids):
        return self.delete(
            self.table_name,
            'id',
            course_ids
        )
