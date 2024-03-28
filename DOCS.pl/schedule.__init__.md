# schedule/__init__.py
  
This file contains Schedule class

---

## SchoolClass
* ### Params:
    * version: schedule_version
    * valid: is this schedule version valid
    * data: schedule data; dict type

* ### Functions
  * ### push_class_schedule
    * ***Params***:
        * class_id: id of passed in class
        * class_schedule: schedule of class to push

    * Usage:
    : self.data[class_id] = class_schedule

    * Return:
    : None
  
  * ### create
      * ***Params***:
          * classes_id: list of ids
          * classes_start_hour_index: dict of hours when class starts
          * conditions: global conditions of schedule
          * days: list of days with lessons in
          * days_ordered: list of days but with order wich in the teachers are added in
          * subjects: split per teacher split per class subjects
          * teachers: list of teachers (obj)
          * log_file_name: file name for run information

      * Return:
      : structured and logical schedule, or False if valid == False.  
      Generation doesn't use any randomnes
  
  * ### split_to_groups
    * ***Params***:
        * days: list of days used in schedule
        * log_file_name: file name for run information

    * Return:
    : schedule with split subjects