# load_data.py
  
This file functions for loading and operating on data

---

* ### Functions
  * ### load_data
      * ***Params***:
          * log_file_name: File, where log data is saved
          * path: path to folder with tables of type CSV or Excel
          * tables: list of files/tables
          * dtype: type of data to read, can be .xlsx/.ods (Excel file), .csv (comma-separated values), defaults to xlsx

      * Return:
      : list of pandas dataframes or False if files don't match schedule data
  
  * ### class_to_dict
      * ***Params***:
          * obj: object
      
      * Usage
      : turns object into python dict

      * Return:
      : object in python dict format
  
  * ### schedule_to_json
     * ***Params*** 
        * schedule: Schedule instance
        * file_path: file path for saving the JSON
     
     * Usage
     : saves schedule into a file   
  
  * ### schedule_to_excel
      * ***Params***:
          * schedule_dict: schedule instance in dict format
          * data: list of raw pandas dataframes (The same order as in generator)
          * info: Arguments (in dict) to write in title page of schedule excel,
            set 'Title' key for a big title; defaults to School Schedule
          * file_path: path where Excel file is saved
      
      * Usage
      : creates Excel file that contains schedule split by classes

      * Return:
      : None