# Developer Tools


>This section is dedicated for developers, 
who look to expand range of programs possibilities

---

## Intro

First download repository through GitHub or clone using command:  
```git clone -b generator git@github.com:OFALOFAL/School.Schedule.Generator.git```

You'll need knowledge of python and excel

To understand flow of program first go to [intro]() section.  

## Intro
Code is split into couple .py files:
* settings
* main
* loadData
* scheduleConditions
* debug_log
* tkinter_schedule_vis
* schoolClass
* subject
* teacher

and one python package:
* schedule

there should also be folder called logs  
> Note:  
> 
> If there is no logs folder, it will be created in process

---

## settings.py
We'll go through all files, but first take a look in settings.py  
This file contains all important global variables, and default names  

Because settings is a constant there is created only one instance
in the same file as definition, so to import settings we import only 
that object as follows:  
`from settings import settings`

---
Settings list:
* DEBUG
: decides workflow of program, mostly regulates logging  

* TKCAPTURE 
: bool to decide if ou want to generate tkinter captures 
of schedule in process of creating schedule, 
more information on this topic in separate chapter

* BASE_DATA_PATH 
: base path of all data used by program

* TEST_DATA_PATH 
: path to data used **only** for testing

* DF_NAMES 
: list of names of all dataframes

* COLUMN_NAMES 
: dictionary with names of dataframes as keys
and corresponding names of theirs columns

> Note:  
> 
> Use ***COLUM NAMES*** re-writing the name rather than pulling it out from 
> setting, this is mainly due to readability and consistency

---

### Program workflow
Next on path to write expansions is to understand the program workflow    
All the code is concentrated in main.py which is the heart of program  
Main contains only one function - generate_schedule
This function is quite complex, so it's worth a while to understand its 
main components  
generate_schedule splits into 3 parts:
* preparing
* creating
* loging
---
***Preparing***  
  
This part of code takes care of preparing, splitting and formatting data
Now we will break down all the lines that are categorized in that group  
```python
now = datetime.now()
time_str = now.strftime("%Y-%m-%d %H-%M-%S.%f")
```
Create current time string for logging (we will take a look on logging in another chapter) 
```python
if not os.path.exists(f'logs/{log_file_name}'):
    os.makedirs(f'logs/{log_file_name}')
with open(f'logs/{log_file_name}/{log_file_name}.txt', 'w') as f:
    pass
```
This part creates directory for log files  
```python
conditions = ScheduleConditions(
    min_lessons_per_day=min_lessons_per_day, 
    max_lessons_per_day=max_lessons_per_day
)
```
This function creates dict of conditions that schedule should follow 
when creating  
```python
[
    lesson_hours_df,
    subject_names_df,
    subjects_df,
    teachers_df,
    classes_df,
    classrooms_df
] = copy.deepcopy(data)

classes_id, classes_start_hour_index = SchoolClass.get_classes_data(classes_df)
teachers = create_teachers(teachers_df)
subjects = split_subjects(subjects_df, teachers, classes_id)
```
This part just splits and formats data  
We won't talk about loading data
as it's not needed and changing it would cause errors 
I'll just mention that this part is in for loop to reset it after every version
of schedule
---
***Creating***  

Before going into code it's good to mention that all the creation is in form
of ***chained functions***
```
schedule = Schedule(valid=False)
for i, days_order in enumerate(permutations(days, len(days))):
    version = i
```
Only thing that can be randomized and has effect on create is **order of days**  
So to be sure that we find if schedule is **possible to create** we iterate 
through **all possibilities** which makes code looking scary and not well optimized (as it is O(n!)) 
but for common 5 days schedule there is only 120 possible versions of schedule
**and** if data is not complex schedule will usually be created in **1st iteration** 

```python
schedule = Schedule(
    version=version
).create(
    classes_id=classes_id,
    classes_starint_hour_index=classes_start_hour_index,
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
    log_file_name=log_file_name
)
```
Now we create Schedule and call all the functions that sequentially 
adds data and formats it as user requests
> Note:  
> 
> To add functionality, you write functions in format_schedule function 
> and not here, this prevents confusion and unwanted bugs 
> (more information in another chapter)

```python
if schedule.valid:
    break
```
Then we check if schedule that we created is valid - if not we continue the loop;
else we break
```python
if not schedule.valid:
    return schedule.valid

return schedule.data
```
after the loop we once again check if schedule is valid - if not return False;
else return raw data of schedule
---
Covering log part won't be necessary as you will read about functions 
in another chapter and functionality will be then straight forward

---

## scheduleConditions.py

This file contains class of the same name which has dictionary with
parameters that schedule has to base on while its creation  
To add parameters first add parameter to `__init__()`  
``def __init__(self, min_lessons_per_day=5, max_lessons_per_day=9, new_value):``  
then add item into `self.data`  
```python
self.data = {
    'min_lessons_per_day': min_lessons_per_day,
    'max_lessons_per_day': max_lessons_per_day,
    "new_value_key": new_value
}
```
lastly add parameter in **main.py** in **generate_schedule**
as follows:  

In function definition
```python
def generate_schedule(
    data, 
    days,
    min_lessons_per_day, 
    max_lessons_per_day, 
    new_value, 
    log_file_name
):
```
In creating conditions object
```python
conditions = ScheduleConditions(
    min_lessons_per_day=min_lessons_per_day, 
    max_lessons_per_day=max_lessons_per_day, 
    new_value=new_value
)
```
... and in call of the function
```python
ss = generate_schedule(
    data=load_data(),
    days=['monday', 'tuesday', 'wednesday', 'thursday', 'friday'],
    min_lessons_per_day=7,
    max_lessons_per_day=10,
    new_value=your_value,
    log_file_name=time_str
)
```

---
## debugLog.py

In this section we'll look into debugLog.py  that contains function of the 
same name  
This is straight forward function as it is an expansion of print,
you pass in file name you want to log information into 
and usual print information
> Note:  
> 
> File will be created in logs folder and print information in the file will be
> split by dashes for readability

---

## tkinter_schedule_vis.py

> Note:  
> 
> To run this function you'll need tkcap library  
> Using pip you can get it with this command:  
> ``pip install tkcap``

Again, straight forward file containing only one function of the same name  
This function will open a new tkinter window, there is many options on how 
it can be done, and you can just read the properties to understand them
---
Properties:
* schedule - schedule object
* days - list of days 
* dir_name (default: 'log_0') - directory to save file to
* capture_name (default: 'tkCapture') - name of the captured screenshot
* capture (default: True) - the same as defining TKCAPTURE in settings,
use it only if you want to in rare conditions 
re-define te settings constant

---

## loadData.py and data classes

Files that we talk about in this section:
* loadData
* schoolClass
* subject
* teacher

As mentioned earlier we won't dive deep into this section 
(especially loadData as this just isn't useful to know) 

Most of the properties in those files are self-explanatory,
so we won't be describing 
all of them just those that can be hard to understand

Dictionary:
* class_signature - full name of class
* max_stack - maximum length that the same subject can appear in a row
* is_empty - if true - this subject will be treated as empty space
* movable - used only on empty spaces, defines if empty can be moved
* group - use if class is splitting to groups for this subject
* number_of_groups - ***used ONLY in create***, defines number of groups
* possible_subjects - list of subjects ids that teacher can teach
* start_hour_index and end_hour_index - time frames of teacher duty for each day
  (in list)
* days - list of days that teacher learns in 

---

## Adding data via excel

To add or delete data you'll just need to add or delete row of data  
It's important to leave column names the same, if not the file won't be read 
properly! 
  
### Columns and their values

> Note:  
> 
> You'll still need to write all the default values!
  
SSG_CLASSES:
* Class_ID - no default, can't repeat values
* grade - can be any (this column isn't important)
* class_sygnature - can be any (this column isn't important)
* class_sygnature_number - can be any (this column isn't important)
* supervising_teacher - can be any (this column isn't important)
* starting_lesson_hour_id - default 0 - decides when class starts it's lessons
  
SSG_CLASSROOMS:
* classroom_ID - no default, can't repeat values
* classroom_name - no default, can't repeat values
* type - no default - decides subjects that can take place in this classroom
  
SSG_CLASSROOMS_TYPES:
* type_ID - no default, can't repeat values
* description - no default - only for visuals
  
SSG_LESSON_HOURS:
* lesson_ID - no default, can't repeat values
* start_hour - time when lesson starts
* duration - duration of lesson
  
SSG_SUBJECT_NAMES:
* subject_name_ID - no default, can't repeat values
* name - no default - only for visuals
  
SSG_TEACHERS:
* teacher_ID - no default, can't repeat values 
* name - no default - only for visuals
* surname - no default - only for visuals
* possible_subjects - no defaults - only for visuals - list of possible subjects
* start_hour_index - list of minimum len of number of active days 
(so for 3 days [a, b, c]) - default for each day is 0
* end_hour_index - similar to start_hour_index - default is -1
* days - similar list to 2 above - 1 if teacher has lessons in that day, else 0
  
SSG_SUBJECTS:
* subject_ID - no default, can't repeat values 
* subject_name_ID - no default - has to exist in SSG_SUBJECT_NAMES
* class_ID - no default - has to exist in SSG_CLASSES
* subject_count_in_week - default 1 - number of times you want to repeat this subject
* number_of_groups - default 1 - number of groups the subject splits class to
* subject_length - no use in code - column has no use
* lesson_hours_ID - this has to always be NULL
* teachers_ID - list of teachers that can take this subject (written like so: [a, b])
* classroom_ID - this has to always be NULL
* max_stack - default 3 - defines how many subject of the same type can be in a row
* classroom_types - list of classroom_types that this subject is in (written like so: [a, b])

---

# Writing new functions


## Part 1: Defining new function

Now, that you know how to move around in project, it's time to write your new function  
To start, first crate new file in `./schedule/format` 
and add function of the same name in it  
then you can import that function in `./schedule/__init__.py` like so:  
```python
from .format.new_file import new_function
```
and add it in format_schedule function:  
```python
return self.update_min_day_len(
        conditions,
        days,
        teachers,
        log_file_name
    ).add_classrooms(
        classrooms,
        days,
        log_file_name
    ).new_function()
```  
and import all data that you need and is aviable in format_schedule to your function:  
```python
).new_function(
  teachers,
  ...,
  log_file_name
)
```
and change it in functions definition:  
```python
def new_function(teachers, ..., log_file_name):
```
For function to work first write this in your function:
```python
if not self.valid:
  return self
  
// Your code here
  
return self
```
---
## Part 2: Logic

Now we'll look at parts of already existing function to see how to operate on subjects  
The function we talk about in this toutorial is update_min_day_len  

Firs look how to loop through subjects data:
```python
for class_schedule, class_id in self.data.items():
  for current_day in days:
      schedule_at_day = class_schedule[current_day]
```
First we loop through items of data to get scoped information,  
then we look only at schedule at speciffic day, this lets us get list of subjects
> Note:  
>   
> By subjects, I mean subjects_list as each item in list is another list  
> That list contains subject objects for each group for this class that has lessons in that time

Then in update_min_day_len we focus on length of day for each class, so we don't loop on subjects
(this is still possible if you need to do operations based on that)
```python
while self.get_num_of_lessons(schedule_at_day, log_file_name) < \
                    conditions.data['min_lessons_per_day']:
  
    // Code to update length of day
    
if self.get_num_of_lessons(schedule_at_day, log_file_name) < conditions.data['min_lessons_per_day']:
    self.valid = False
    return self
```
We update length of day until it's ready, or it's not possible
> ### Important!  
>  
> **It's very important to know when your function is declared failed**,  
> ***If that happends you need to write those 3 lines:***
> ```python
> if your_condition:
>    self.valid = False
>    return self
> ```
> **If for some reason you can't declare function failed then make sure that** ***it doesn't loop to infinity!***

Now a qiuck summary of code inside of update_min_day_len function just 
to give you a hint on how to write your function  

We first find the longest day for that class to take subject from (this is an optimal case)  
```python
max_len_day_i = class_schedule_list.index(max(class_schedule.values(), key=len))
```
and we try to move last lesson from it to the current day to make that days lenght one longer
```python
if self.safe_move(
    teachers_id=max_day_schedule[-1][0].teachers_id,
    day_from=days[max_len_day_i],
    day_to=current_day,
    subject_position=-1,
    subject_new_position=-1,
    class_id=class_id,
    days=days,
    teachers=teachers,
    log_file_name=log_file_name
):
```
if that doesn't work we check and try to add first or last lesson 
from the longest day to first or last index of current day:
```python
elif self.safe_move(
    ...,
    subject_position=first_lesson_index,
):
```
then, if that doesn't work, we do the same thing but for all the other days  
if none of the days in this class schedule can add to the day in need than that schedule is 
declared not valid  
In other words, if there is no possibility to complete the minimum length requirement, than
we fail the current schedule and try to create another one with diffrent day order 
(look at main.py explenation)
