# settings.py

This file contains all important global variables, and default names  

Because settings is a constant there is created only one instance
in the same file as definition, so to import settings, import only 
that object instance as follows:  
`from settings import settings`

---
Settings list:
* DEBUG
: decides workflow of program, use in testing

* TKCAPTURE 
: bool to decide if ou want to generate tkinter captures 
of schedule in process of creating schedule, 
more information on this topic in separate chapter

* SAVELOG  
: bool to decide if debuglog saves logs in a file

* BASE_DATA_PATH 
: base path of all data used by program

* TEST_DATA_PATH 
: path to data used **only** for testing

* DF_NAMES 
: list of names of all dataframes

* COLUMN_NAMES 
: dictionary with names of dataframes as keys
and corresponding names of theirs columns

> [!NOTE]  
> Use ***COLUM NAMES*** re-writing the name rather than pulling it out from setting  
> Do it for readability and consistency