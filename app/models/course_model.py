import json

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
