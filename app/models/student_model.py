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

    def add(self):
        self.create(
            self.table_name,
            self.to_dict()
        )

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
