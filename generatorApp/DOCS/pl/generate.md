# generate.py
  
This file contains generate function and test usage of program

---

## generate
  * ***Params***:
      * data: list of data in strict order of:  
        ```python
        [  
            lesson_hours_df,  
            subject_names_df,  
            subjects_df,  
            teachers_df,  
            classes_df,  
            classrooms_df  
        ] 
        ```
        
      * log_file_name: current time for logging
      * schedule_settings: dictionary of settings for schedule
    
  * Usage:
  : generates a full schedule for all the classes where none of the same elements (teachers/clasrooms) appears
    in the same time
    
  * Return:
  : Schedule instance

--- 

# File explained line-by-line:

## Starting from line 106:

### Set data for logs
```python
    now = datetime.now()
    time_str = now.strftime("%Y-%m-%d %H-%M-%S.%f")
```

### Load data 
and proceede if data loaded propearly
```python
    data = load_data(time_str)
    if data:
        (...)
    else:
        print("Error; couldn't load data", file=sys.stderr)
```

### Set settings
```python
    schedule_settings = {
            'days': ['monday', 'tuesday', 'wednesday', 'thursday', 'friday'],
            'min_lessons_per_day': 7,
            'max_lessons_per_day': 10
        }
```

### Generate schedule
```python
    schedule = generate_schedule(
            data=data,
            schedule_settings=schedule_settings,
            log_file_name=time_str
        )
```

---
## Now we get to the function:


### Define helping function
This function returns tuple of every possible order of list items,
it's important for creating day orders in later part of program.
```python
    def permutations(iterable, r=None):
    pool = tuple(iterable)
    n = len(pool)
    r = n if r is None else r
    for indices in product(range(n), repeat=r):
        if len(set(indices)) == r:
            yield tuple(pool[i] for i in indices)
```

### Pull settings from dict
```python
    min_lessons_per_day, max_lessons_per_day = schedule_settings["min_lessons_per_day"], schedule_settings["max_lessons_per_day"]
    days = schedule_settings["days"]
```

### Create directory for log files
```python
    if not os.path.exists(f'logs/{log_file_name}'):
        os.makedirs(f'logs/{log_file_name}')
    with open(f'logs/{log_file_name}/.log', 'w') as f:
        pass
```

### Create global schedule conditions
```python
    conditions = ScheduleConditions(min_lessons_per_day=min_lessons_per_day, max_lessons_per_day=max_lessons_per_day)
```

### Set schedule variable
```python
    schedule = False
```

### Loop through every combination of days
Days order is only thing that makes schedule generation random,
so if we loop through every possible order, until we get working schedule,
we can be sure that we didn't miss anything
```python
    for i, days_order in enumerate(permutations(days, len(days))):
        version = i
```

### Split data to separate dataframes
```python
    [
        lesson_hours_df,
        subject_names_df,
        subjects_df,
        teachers_df,
        classes_df,
        classrooms_df,
        classroom_types_df
    ] = copy.deepcopy(data)
```

### Gather data from dataframes
```python
    classes_id, classes_start_hour_index = SchoolClass.get_classes_data(classes_df)
    teachers = create_teachers(teachers_df)
    subjects = split_subjects(subjects_df, teachers, classes_id)
    classrooms = create_classrooms(classrooms_df)
```

### Generate schedule
```python
    schedule = Schedule(version=version).create(
        classes_id=classes_id,
        classes_start_hour_index=classes_start_hour_index,
        conditions=conditions,
        days=days,
        days_ordered=days_order,
        subjects=subjects,
        teachers=teachers,
        log_file_name=log_file_name
    ).split_to_groups(
        days,
        conditions,
        log_file_name
    ).format_schedule(
        conditions,
        days=days,
        teachers=teachers,
        classrooms=classrooms,
        classes_id=classes_id,
        classes_start_hour_index=classes_start_hour_index,
        days_ordered=days_order,
        log_file_name=log_file_name
    )
```

### Log if schedule version was valid
```python
    debug_log(log_file_name, f"Version: {version}, Valid: {schedule.valid}, Day order: {days_order}")
```

### Brake from loop if schedule is valid
While creating schedule, functions keep track of schedule validation and set schedule valid variable appropriately.
```python
    if schedule.valid:
        break
```

### Create tkinter visualisation of valid (or last) schedule:
```python
    # schedule visualisation using tkinter
    if not tkinter_schedule_vis(
        schedule=schedule,
        days=days,
        dir_name=f'{log_file_name}',
        capture_name='FinalCapture',
        capture=True
    ):
        debug_log(log_file_name, 'DEBUG: no tkinter generated')

```

### Return schedule data
Returning only raw schedule as other things aren't necessary
```python
    return schedule.data
```