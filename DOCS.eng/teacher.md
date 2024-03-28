# teacher.py
  
This file contains Teacher class

---

## Teacher
* ### Params:
    * name: teacher name
    * surname: teacher surname
    * possible_subjects: list of subjects that the teacher can teach
    * start_hour_index: hour id, decides when teacher starst lessons (can start later)
    * end_hour_index: hour id, decides when teacher end lessons (can start earlier)

## create_teachers
  * ***Params***:
      * teachers_df: dataframe of all teachers

  * Usage:
  : turn pandas df data to class instances  

  * Return:
  : dict of every teacher, key - teacher_id