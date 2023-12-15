class SchoolClass:
    """
    :description: class from classes dataframe turned into an object
    """
    def __init__(self, class_id, grade, class_signature, supervising_teacher):
        self.class_id = class_id
        self.grade = grade
        self.class_signature = class_signature
        self.supervising_teacher = supervising_teacher

    @staticmethod
    def get_classes_data(df):
        """
        :param df: dataframe of classes
        :return: list of classes ids and dict of hours when class starts
        """
        classes_start_hour_index = {}
        for i, class_id in enumerate(df['Class_ID'].to_numpy()):
            classes_start_hour_index[class_id] = df['starting_lesson_hour_id'].to_numpy()[i]

        return df['Class_ID'].to_numpy(), classes_start_hour_index

    @staticmethod
    def get_school_classes(class_df, classes_id):
        """
        :param class_df: dataframe of all classes
        :param classes_id: list of classes ids
        :return: returns dict of every class
        """
        school_classes = [SchoolClass(
                class_id=class_df.loc[i, 'Class_ID'],
                grade=class_df.loc[i, 'grade'],
                class_signature=class_df.loc[i, 'class_signature'],
                supervising_teacher=class_df.loc[i, 'supervising_teacher']
            )
            for i, class_id in enumerate(classes_id)
        ]
        return school_classes
