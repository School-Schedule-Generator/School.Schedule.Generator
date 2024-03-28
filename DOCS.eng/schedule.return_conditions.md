# schedule/__init__.py
  
This file contains Schedule class functions for checking if conditions are met

---

## Functions
  * ### are_teachers_taken
    * ***Params***:
        * teachers_id: teachers id
        * day: day of new subject position
        * lesson_index: index of new subject position

    * Usage:
    : check if teachers at passed in new position have already lessons.
    This function is for checking if it's possible to change subject position

    * Return:
    : True/False depending on if teachers have already lessons at passed in position

  * ### check_teacher_conditions
    * ***Params***:
        * teachers_id: teachers id
        * day: day of teachers new subject position
        * days: list of days
        * lesson_index: index of new subject position
        * teachers: list of all teachers

    * Usage:
    : if teacher had a subject at passed position, would it conflict with his working conditions

    * Return:
    : True if conditions are met; else False
