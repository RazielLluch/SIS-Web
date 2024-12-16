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
