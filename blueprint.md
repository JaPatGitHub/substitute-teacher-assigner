# School Substitute Teacher Assigner (Blueprint)

## Objective

Our software will automate the process of assigning substitute teachers for absentee teachers on a given school day. 
It will also seek to ensure the comfort of teachers  by assigning periods to those with:

1. the lowest number of existing periods, and
2. the highest possible gap between teaching and substitution periods

### Additional Functionalities

The software will also enable to:

1. make user-friendly changes to the standard timetables.
2. maintain date-wise records.
3. send e-mails to the teachers who are assigned as substitutes.

## Components

1. **`__main__` Program:**  Interacts with the user. Also integrates all the functionalities provided by the other components.

2. **Standard Data Directory:** Contains the daily timetables and list of teachers with email information and notification choice.

3. **Operational Database:** Fetches standard data and allows making required changes for the procedure.

4. **Assignment Module:** Contains the algorithms for assigning substitute teachers.

5. **`MySQL` Simplified Module:** Built on top of the `MySQL.connector` module.
It simplifies the execution of queries required in the module.

6. **Date & File handling Module:** Built on top of the `datetime` and `csv` modules.
It provides functions for managing daily records.

7. **Email Functionalities Module:** Built on the top of `smtplib` module.
It provides functions to send emails to substitute teachers.

8. **Records Directory:** Stores date-wise records of absent and substitute teachers.

## Algorithm

This is an algorithm for the overall process:

**_Step 1:_** Fetch the particular day's timetable and the teacher list from the standard data to the operational database.

**_Step 2:_** Show the user the existing data and confirm with them if it is correct.
If not, i) drop the tables from the operational database and ii)ask the user to correct the standard data. Exit the program in this case

**_Step 3:_** Ask the user to list the absent teachers (by numerical reference).
Confirm with the user.

**_Step 4:_** Duplicate the table with the standard timetable. In the duplicated table, nullify the fields containing the absent teachers.

**_Step 5:_** Calculate the _number of periods requiring substitution_, say `num_subst` (by counting the number of null values).

**_Step 6:_** Create a dictionary, say `period_load`. Let the _number of periods_ be the keys and the _list of teachers teaching those many periods_ be the values. ( by calculating the number of times their name appears on the table)

```python
period_load = {1: [], 2:[], 3:[], 4:["teacher_x"] 5:["teacher_y", "teacher_z"], ...}
```

**_Step 7:_** Create another dictionary, say `subsititutes_pool`.
It will contain the names of teachers to be given substitute periods.
The structure will be similar to the above dictionary.

This can be done by creating a variable, say `counter`.
Add key-value pairs from `period_load` to `substitute_pool` with increasing order of keys.
Every time this happens, double the value of `counter` and add the length of the value list to it.
Continue the process till the value of `counter > num_substitutes`.

```python
# Considering num_substitutes = 4
subst_pool = {4:["teacher_x"] 5:["teacher_y", "teacher_z"]}
```

**_Step 8:_** Store the maximum value of the keys of the `subst_pool` dictionary in a variale, say `max_subst_load`.

**_Step 9:_** Create another dictionary, say `subst_details`.
Here, names of each teacher from `subst_pool` will be the keys.
The values will be a list consiting of 2 nested lists.
The first nested list will contain all the periods the teacher is engaged in

```python
subst_details = {
    "teacher_x":[[1, 3, 7, 8], []]
    "teacher_y":[[1, 4, 6, 7, 8], []]
    "teacher_z":[[1, 2, 3, 5, 6], []]
}
```

**_Step 10:_** For every vacant period (i.e. null value), calculate the least distance between that period and each teacher's existing periods.
Store the value otained in the second nested list.

```python
# Consider period 3 is vacant at some class
subst_details = {
    "teacher_x":[[1, 3, 7, 8], [2]]
    "teacher_y":[[1, 4, 6, 7, 8], [1]]
    "teacher_z":[[1, 2, 3, 5, 6], [0]]
}
```

**_Step 11:_** Assign the period to the teacher with the maximum distance as obtained in the above step.

**_Step 12:_** Add the newly assigned period to the teacher's first nested list in `subst_details`.
However, if the length of the list is greater than the value of `max_subst_load`, delete the key-value pair so that no more periods are substituted to the teacher.

```python
# Let period to subst_pool = {4:[] 5:["teacher_y", "teacher_z", "teacher_x"]}e assigned to teacher_x
subst_details = {
    "teacher_x":[[1, 3, 7, 8, 2], [2]]
    "teacher_y":[[1, 4, 6, 7, 8], [1]]
    "teacher_z":[[1, 2, 3, 5, 6], [0]]
}
```

**_Step 13:_** Repeat steps 10 to 12 till all vacant periods are assigned.

**_Step 14:_** Display users the new time table. Allow changes according to their preference.

**_Step 15:_** Compare the standard and new timetable and create a table with records containing period number, class, absent teacher and substitute teacher. Assign the column with substitue teachers as foreign key.

**_Step 16:_** Generate a `csv` file from the above table and store it in the records directory.

**_Step 17:_** Ask the user if they wish to notify the substitute teachers using email. If yes, natural join the above tale and the table containing teacher list. Then send email to the teachers who have opted for email notification.
