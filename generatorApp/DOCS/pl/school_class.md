# school_class.py
  
This file contains SchoolClass class

---

## SchoolClass
* ### Params:
    * class_id
    * grade (**1**a, **2**a, **2**b)
    * class_signature (1**a**, 1**b**, 1**c**)
    * supervising_teacher

* ### Functions
  * get_classes_data
    * ***Params***:
        * df: dataframe of classes

    * Usage:
    : get all class_ids

    * Return:
    : list of classes ids and dict of hours when class starts
  
  * get_school_classes
      * ***Params***:
          * class_df: dataframe of all classes
          * classes_id: list of classes ids

      * Usage:
      : turn pandas df data to class instances  

      * Return:
      : dict of every class