class SchoolClass:
    """
    class from classes dataframe turned into an object
    """
    def __init__(self, class_id, grade, class_signature, supervising_teacher):
        self.class_id = class_id
        self.grade = grade
        self.class_signature = class_signature
        self.supervising_teacher = supervising_teacher

    @staticmethod
    def get_classes_id(df):
        """
        :param df: dataframe of classes
        :return: list of classes ids
        """
        return df['Class_ID'].to_numpy()
