# subject.py
  
This file contains class Subject

---

## Subject
* ### Params:
    * subject_id
    * subject_name_id: id of name
    * class_id: id of class
    * number_of_groups: number of groups that the class splits into for this subject
    * lesson_hour_id: id of lesson hour
    * teachers_id: id of teacher, if None defaults to [-1]
    * classroom_id: id of classroom
    * is_empty: if True, this instance is an empty subject 
      (used to make space before lessons for class start)
    * max_stack: number to decide how many subjects of this type can be in a row
    * movable: decides if this subject can be moved
    * group: group that this subject is for when class is split into groups
    * classroom_types: type of classroom

* ### Functions
  * ### split_subjects
      * ***Params***:
          * subjects_df: dataframe of all subjects
          * teachers: list of school_classes
          * classes_id: list of ids of classes

      * Usage:
      : turn pandas df data to class instances  

      * Return:
      : split by teachers and by classes ([teacher_id][class_id]) lists of subjects