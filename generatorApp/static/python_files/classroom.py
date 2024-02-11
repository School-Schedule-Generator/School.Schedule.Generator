class Classroom:
    def __init__(self, classroom_name, type_id):
        self.classroom_name = classroom_name
        self.type_id = type_id


def create_classrooms(classrooms_df):
    classrooms = {}
    for _, row in classrooms_df.iterrows():
        classrooms[row['classroom_id']] = Classroom(
            classroom_name=row['classroom_name'],
            type_id=row['type_id']
        )

    return classrooms
