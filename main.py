import sys
import sqlsimp as sql
import datesimp as date
import assignment as asg

print("Hello! Welcome to school substitute assigner")
print("Today is {0}, {1} {2}, {3}".format(date.get_weekday().capitalize(), date.get_day(), date.get_month(), date.get_year()))
input("Press Enter to continue")
print()

sql.connect_sql()
sql.use_db("subst_assignment")

tt_file = "standard-details\\{0}.csv".format(date.get_weekday())
tt_table_std = "{0}{1}{2}std".format(date.get_year(), date.get_month(), date.get_day()) # Standard Timetable
tt_table_func = "{0}{1}{2}func".format(date.get_year(), date.get_month(), date.get_day()) # Functional Timetable

list_file = "standard-details\\list.csv"
list_table = "list{0}{1}{2}".format(date.get_year(), date.get_month(), date.get_day()) # teacher's list

try:
    sql.csv_to_sql(tt_file, tt_table_std)
    sql.csv_to_sql(tt_file, tt_table_func)
    
    sql.csv_to_sql(list_file, list_table)
    
except:
    print("""There is some problem in the format of file stored at {0} or {1}
Process terminated
Kindly sort out and try again""".format(tt_file, list_file))
    input()
    sys.exit()
    
tt = sql.read_table(tt_table_std)
t_list = sql.read_table(list_table)

for e in tt:
    line = ""
    for f in e:
        line += "%10s"%f
    print(line)
print()

print("""Pleases check if today's standard time table is correct.
If not, enter NO to terminate this process. Kindly correct the details stored at {0} and restart.
If yes, enter YES to continue""".format(tt_file))

while True:
    ch = input()
    
    if ch.lower() in ["yes", "y"]:
        break
    elif ch.lower() in ["no", "n"]:
        
        sql.drop_table(tt_table_std)
        sql.drop_table(tt_table_func)
        sql.drop_table(list_table)
        
        sys.exit()
        
    else:
        print()
        print("Please enter YES or NO")

proceed = asg.check_list(tt, t_list)

if proceed == False:
    print("Kindly correct and try again")
    input()
    sys.exit()
    

    


        

        

        
        
        
        
        

   