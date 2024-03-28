# schedule/general.py
  
This file contains Schedule class general functions

---

## Functions
  * ### create_class_schedule
    * ***Params***:
        * days: list of days that the lessons can be in

    * Return:
    : empty schedule of passed in days
  
  * ### move_subject_to_day
    * ***Params***:
        * class_id: id of current class
        * day_to: day to move subject to
        * day_from: subject current day position
        * subject_position: subject position in day
        * subject_to_position: can be -1 or first lesson index; 
      decides where subject is moved to

    * Usage:
    : self.data[class_id] = class_schedule

    * Return:
    : True if moving was succesfull, else False
  
  * ### swap_subject_in_groups
    * ***Params***:
        * group: group id (not an index)
        * subjects_list_x, subjects_list_y: subject to swap

    * Usage:
    : swaps subject positions

    * Return:
    : None
  
  * ### safe_move
    * ***Params***:
        * teachers_id: ids of teachers to check
        * day_from: day which we take subject from
        * day_to: day which we add subject to
        * subject_position: old position of subject
        * subject_new_position: new position to add subject to
        * class_id: class of subject moved
        * days: list of days
        * teachers: list of all teachers
        * group: class group to move
        * log_file_name: file name for run information

    * Usage:
    : before trying to move using move_subject_to_day(), function checks if action is possible
    and notifies program

    * Return:
    : bool; was operation successful

  * ### get_same_time_teacher
    * ***Params***:
        * day: day of subject
        * lesson_index: index of subject

    * Return:
    : list of teachers that have lesson at day at lesson index
  
  * ### get_same_time_classrooms
    * ***Params***:
        * day: day of subject
        * lesson_index: index of subject

    * Return:
    : list of classrooms that have lesson at day at lesson index

  * ### get_stacked_lessons
    * ***Params***:
        * class_id: class id
        * day: day of subject
        * group: group of subject
        * lesson_index: index of subject; if == 0 then defaults to first lesson index
        * log_file_name: file name for run information

    * Usage:
    : check if subject reached limit of max_stack

    * Return:
    : list of the same subject type in a row, last subjects in stack lesson hour index

  * ### find_another_grouped_lessons
    * ***Params***:
        * class_id: class id
        * lesson_day: day of subject
        * number_of_groups: numer of groups of this subject
        * lesson_index: index of subject
        * days: list of days

    * Usage:
    : check if any lesson is split into groups, 
    this if for swapping out the grouped subject so teacher doesn't have 2 lessons simultaneously

    * Return:
    : list of the grouped lessons that can be swapped with another grouped lesson

  * ### find_first_lesson_index
    * ***Params***:
        * schedule_at_day: schedule[class_id][day]
        * log_file_name
    
    * Usage:
    : find firs lesson index as if there is an empty subject the index won't be 0
    
    * Return:
    : index or None if day is empty

  * ### get_num_of_lessons
    * ***Params***:
        * schedule_at_day: schedule[class_id][day]
        * log_file_name
    
    * Return:
    : number of not empty lessons in a day