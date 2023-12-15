# Developer Tools


>This section is dedicated for developers, 
who look to expand range of programs possibilities.

---

## Intro

First download repository through GitHub or clone using command:  
```git clone -b generator git@github.com:OFALOFAL/School.Schedule.Generator.git```

You'll need knowledge of python and excel.

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
This file contains all important global variables, and default names.  

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
> setting, this is mainly due to readability and consistency.

---

### Program workflow
Next on path to write expansions is to understand the program workflow.    
All the code is concentrated in main.py which is the heart of program.  
Main contains only one function - generate_schedule.
This function is quite complex, so it's worth a while to understand its 
main components.  
generate_schedule splits into 3 parts:
* preparing
* creating
* loging
---
***Preparing***  
  
This part of code takes care of preparing, splitting and formatting data.
Now we will break down all the lines that are categorized in that group  
```
now = datetime.now()
time_str = now.strftime("%Y-%m-%d %H-%M-%S.%f")
```
Create current time string for logging (we will take a look on logging in another chapter) 
```
if not os.path.exists(f'logs/{log_file_name}'):
    os.makedirs(f'logs/{log_file_name}')
with open(f'logs/{log_file_name}/{log_file_name}.txt', 'w') as f:
    pass
```
This part creates directory for log files  
```
conditions = ScheduleConditions(
    min_lessons_per_day=min_lessons_per_day, 
    max_lessons_per_day=max_lessons_per_day
)
```
This function creates dict of conditions that schedule should follow 
when creating  
```
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
This part just splits and formats data. We won't talk about loading data
as it's not needed and changing it would cause errors. 
I'll just mention that this part is in for loop to reset it after every version
of schedule
---
***Creating***  

Before going into code it's good to mention that all the creation is in form
of ***chained functions***.
```
schedule = Schedule(valid=False)
for i, days_order in enumerate(permutations(days, len(days))):
    version = i
```
Only thing that can be randomized and has effect on create is **order of days**.  
So to be sure that we find if schedule is **possible to create** we iterate 
through **all possibilities** which makes code looking scary and not well optimized (as it is O(n!)) 
but for common 5 days schedule there is only 120 possible versions of schedule
**and** if data is not complex schedule will usually be created in **1st iteration**. 

```
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
adds data and formats it as user requests.
> Note:  
> 
> To add functionality, you write functions in format_schedule function 
> and not here, this prevents confusion and unwanted bugs. 
> (more information in another chapter)

```
if schedule.valid:
    break
```
Then we check if schedule that we created is valid - if not we continue the loop;
else we break
```
if not schedule.valid:
    return schedule.valid

return schedule.data
```
after the loop we once again check if schedule is valid - if not return False;
else return raw data of schedule
---
Covering log part won't be necessary as you will read about functions 
in another chapter and functionality will be then straight forward.

---

## scheduleConditions.py

This file contains class of the same name which has dictionary with
parameters that schedule has to base on while its creation.  
To add parameters first add parameter to `__init__()`  
``def __init__(self, min_lessons_per_day=5, max_lessons_per_day=9, new_value):``  
then add item into `self.data`  
```
self.data = {
    'min_lessons_per_day': min_lessons_per_day,
    'max_lessons_per_day': max_lessons_per_day,
    "new_value_key": new_value
}
```
lastly add parameter in **main.py** in **generate_schedule**
as follows:  

In function definition
```
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
```
conditions = ScheduleConditions(
    min_lessons_per_day=min_lessons_per_day, 
    max_lessons_per_day=max_lessons_per_day, 
    new_value=new_value
)
```
... and in call of the function
```
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
> split by dashes for readability.

---

## tkinter_schedule_vis.py

> Note:  
> 
> To run this function you'll need tkcap library.  
> Using pip you can get it with this command:  
> ``pip install tkcap``

Again, straight forward file containing only one function of the same name.  
This function will open a new tkinter window, there is many options on how 
it can be done, and you can just read the properties to understand them.
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
all of them just those that can be hard to understand.

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

To add or delete data you'll just need to add or delete row of data.  
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

Now, that you know how to move around in project, it's time to write your new function.  
To start, first crate new file in `./schedule/formatFunctions` 
and add function of the same name in it  
then you can import that function in `./schedule/formatschedule.py` like so:  
(dodaj import)  
`  `  
and add it in format_schedule function:  
(dodaj formatowanie)  
`  `  
and import all data that you need and is aviable in format_schedule to your function:
(dodaj dodawanie danych)
`  `  
and change it in functions definition:
`  `  
in start of your function you'll need to write those three lines:
```
if not self.valid:
  return self
  
  //Your code here
  
return self
```
> Note:
> 
> You can write your formatting in between if-statement and 2nd return

(DO KONTYNUACJ, wyjaśnić jak pisać funkcje, jak loopować itd)
