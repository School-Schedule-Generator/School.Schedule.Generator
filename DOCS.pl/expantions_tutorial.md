### Create expansions

To write expansions first get to know the project by reading files documentation 
and then follow this tutorial.

First download the project branch from GitHub as zip or clone it with this command:  
`git clone -b generator git@github.com:School-Schedule-Generator/School.Schedule.Generator.git`  

Then using pip (or other package installer) get the requirements from requirements.txt  
`pip install -r requirements.txt`  

#### We are ready to go!

Your expansion will be placed in schedule/format/

First open a template (template.py); this is code inside of it:
```python
def <FUNCTION NAME>(self, <PARAMETERS>, log_file_name):
	
    # don't delete
    if self.valid is False:
        return self

    # YOUR LOGIC HERE

    return self # don't delete
```

Set your function name then copy your template to that directory and rename it to the same name as function.  
As parameters set all the dataframes and objects provided by format_schedule function (in schedule/format/format_schedule.py).  
e.g.:
```python
def update_min_day_len(self, conditions, days, teachers, log_file_name):
```

Go to schedule/__init__.py and import your function in class like that:  
```python
class Schedule:
    (...)
    from .format.update_min_day_len import update_min_day_len
    
    from .format.<FUNCTION NAME> import <FUNCTION NAME>
```

After that go to schedule/format/format_schedule.py and add your function implementation (with all the parameters)
to the return statement after other format functions seperated by "." like that:
```python
return self.update_min_day_len(
        conditions,
        days,
        teachers,
        log_file_name
    ).add_classrooms(
        classrooms,
        teachers,
        days
    ).<FUNCTION NAME>(
        <PARAMETERS>, 
        log_file_name
    )
```

#### And that's pretty much it
If you have any problems, remember that you can use every function provided by us in schedule.  
e.g.:
```python
    self.get_num_of_lessons(schedule_at_day, log_file_name)
```

Thank you for choosing our program :)  
If you create any cool expansion feel free to contact us and make the expansion official.
