
import sys
import sqlsimp as sql
import datesimp as date

def display_tt(tt_list):
    for e in tt_list:
        line = ""
        for f in e:
            line += "%10s"%f
        print(line)

def check_list(tt_list, teachers_list):
    teachers = []
    not_found = []

    for i in range(1, len(teachers_list)):
        teacher = teachers_list[i][1].lower()
        teachers.append(teacher)
        
    for i in range(1, len(tt_list)):
        for j in range(1, len(tt_list[i])):
            if tt_list[i][j].lower() in teachers:
                continue
            else:
                if tt_list[i][j] not in not_found:
                    not_found.append(tt_list[i][j])
                
    if len(not_found) == 0:
        return True
    else:
        print("The following names are not found in the list:")
        for e in not_found:
            print(e)
        return False
    
def obtain_absentees(teachers_list):
    print()
    for e in teachers_list:
        print("%5s"%e[0], "%30s"%e[1])
    print()
    
    absent_no = eval(input("Enter the serial no. of absentees separated by commas (Eg: 2,5,7): "))
    
    if type(absent_no) == int:
        absent_no = absent_no,

    absentees = []
    for e in absent_no:
        absentees.append(teachers_list[e][1])
    
    return absentees

def tt_details(tt):
    teachers_asg = {} # periods the teachers are already assigned
    period_load = {} # teachers having a particular no. of periods
    subst_requirement = {'class_index' : [], 'periods' : []}

    for i in range(1, len(tt)):
        period = i
        period_load[i] = []

        for j in range(1, len(tt[i])):
            class_index = j
            teacher = tt[i][j]
            
            if tt[i][j] == None:
                subst_requirement['class_index'].append(class_index)
                subst_requirement['periods'].append(period)
                continue

            elif teacher in teachers_asg.keys():
                teachers_asg[teacher].append(period)

                new_load = len(teachers_asg[teacher])
                old_load = new_load - 1

                period_load[old_load].remove(teacher)
                period_load[new_load].append(teacher)
                
            else:
                teachers_asg[teacher] = [period]
                period_load[1].append(teacher)

    num_subst = len(subst_requirement["periods"]) 
                
    return teachers_asg, period_load, subst_requirement, num_subst
    
def find_subst_teachers(period_load, num_subst):
    subst_teachers = []
    count = 0

    periods = list(period_load.keys())
    periods.sort()

    for e in periods:
        if count > num_subst:
            break
        else:
            subst_teachers.extend(period_load[e])
            count += len(subst_teachers)

    return subst_teachers

def assign_subst(tt_table, subst_requirement, subst_teachers, teachers_asg):
    subst_details = {}
    class_list = sql.read_table(tt_table)
    class_list = class_list[0]

    for teacher in subst_teachers:
        subst_details[teacher] = teachers_asg[teacher]
      
    max_subst_load = 0
    for e in subst_details.values():
        if len(e) > max_subst_load:
            max_subst_load = len(e)
    
    for i in range(len(subst_requirement["periods"])):
        period = subst_requirement["periods"][i]
        class_index = subst_requirement["class_index"][i]
        class_name = class_list[class_index]

        min_dist_list = [] #List of minimimum distance of all teachers from period
        min_t_list = [] #Teacher list corresponding to above

        for teacher in subst_details:

            if len(subst_details[teacher]) > max_subst_load:
                del subst_details[teacher]
                continue

            dist_list = [] #List of ditances from all periods of teacher
            
            for e in subst_details[teacher]:
                dist = abs(e - period)
                dist_list.append(dist)

            min_dist = min(dist_list)
            min_t_list.append(teacher)
            min_dist_list.append(min_dist)
        
        ideal_dist = max(min_dist_list) # Maximum of the list conataining minium distances
        subst_t_index = min_dist_list.index(ideal_dist)
        subst = min_t_list[subst_t_index]
        
        sql.modify_val(tt_table, class_name, subst, "periods", period)

def modify_tt(tt_table):
    tt = sql.read_table(tt_table)
    proceed = False
    
    while proceed == False:
        try:
            print()
            period = int(input("Enter the period you want to modify: "))
            class_name = input("Enter the class you want to modify: ")
            
            if period > len(tt)-1:
                print("Please enter a value within", len(tt)-1)
                continue
            
            if class_name not in tt[0]:
                print("The class you entered does not exist")
                
            proceed = True
            
        except:
            print("Please enter a valid integer")

        teacher = input("Enter the name of teacher you wish to assign: ")

    sql.modify_val(tt_table, class_name, teacher, "periods", period)

def compare_tt(tt_table_std, tt_table_func):
    tt_std = sql.read_table(tt_table_std)
    tt_func = sql.read_table(tt_table_func)

    sql.create_table(subst_table, ["Period", "Class", "Absent_Teacher", "Substitute_Teacher"], ["int", "varchar(50)", "varchar(50)", "varchar(50)"])

    for period in range(1, len(tt_std)):
        for class_name in range(1, len(tt_std[period])):
            if tt_std[period][class_name] != tt_func[period][class_name]:
                sql.insert_values(subst_table, [period, tt_std[0][class_name], tt_std[period][class_name], tt_func[period][class_name]])

    return subst_table
      

# __main__

print("Hello! Welcome to school substitute assigner")
print("Today is {0}, {1} {2}, {3}".format(date.get_weekday().capitalize(), date.get_day(), date.get_month(), date.get_year()))
input("Press Enter to continue")
print()

sql.connect_sql()
sql.use_db("subst_assignment")

tt_file = "standard-details\\{0}.csv".format(date.get_weekday())
tt_table_std = "{0}{1}{2}std".format(date.get_year(), date.get_month(), date.get_day()) # Standard Timetable
tt_table_func = "{0}{1}{2}func".format(date.get_year(), date.get_month(), date.get_day()) # Functional Timetable

teachers_file = "standard-details\\list.csv"
teachers_table = "list{0}{1}{2}".format(date.get_year(), date.get_month(), date.get_day()) # teacher's list

subst_table = "{0}{1}{2}subst".format(date.get_year(), date.get_month(), date.get_day())
csv_file = f"record\\{date.get_year()}{date.get_month()}{date.get_day()}.csv"

if sql.check_table_exists(subst_table):
    print("You have already generated substitue list for today")
    print("Please check is it is stored at", csv_file)
    
    ch = input("Enter 'yes' is you wish to regenerate. Or press ENTER to exit: ")
    
    if ch.lower() in ["yes", "y"]:
        
        sql.drop_table(tt_table_std)
        sql.drop_table(tt_table_func)
        sql.drop_table(subst_table)
        sql.drop_table(teachers_table)
        
    else:
        sys.exit()

try:
    sql.csv_to_sql(tt_file, tt_table_std)
    sql.csv_to_sql(tt_file, tt_table_func)
    
    sql.csv_to_sql(teachers_file, teachers_table)
    
except:
    print("""There is some problem in the format of file stored at {0} or {1}
Process terminated
Kindly sort out and try again""".format(tt_file, teachers_file))
    input()
    sys.exit()
    
tt_std = sql.read_table(tt_table_std)
teachers_list = sql.read_table(teachers_table)

display_tt(tt_std)
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
        sql.drop_table(teachers_table)

        print()
        print("Process terminated")
        
        sys.exit()
        
    else:
        print()
        print("Please enter YES or NO")

proceed = check_list(tt_std, teachers_list)

if proceed == False:
    print("Kindly correct and try again")
    input()
    sys.exit()

absentees = obtain_absentees(teachers_list)
sql.nullify_val(tt_table_func, absentees)

tt_func = sql.read_table(tt_table_func)

teachers_asg, period_load, subst_requirement, num_subst = tt_details(tt_func)
subst_teachers = find_subst_teachers(period_load, num_subst)
assign_subst(tt_table_func, subst_requirement, subst_teachers, teachers_asg)

tt_func = sql.read_table(tt_table_func)
print()
print("This is the final timetable for today:")
print()
display_tt(tt_func)

print()
while True:
    modify = input("Do you wish to make any modifications: ")
    
    if modify.lower() in ["no", "n"]:
        break
    
    elif modify.lower() in ["yes", "y"]:
        modify_tt(tt_table_func)
        tt_func = sql.read_table()
        display_tt(tt_func)
        
    else:
        print("Please enter 'yes' or 'no'")
        
subst_table = compare_tt(tt_table_std, tt_table_func)
subst_list = sql.read_table(subst_table)

sql.sql_to_csv(subst_table, csv_file)

print("This is the final substitute list:")
print()
display_tt(subst_list)
print()

print("Your file has been stored at", csv_file)
print("Thank you for using this software. Have a nice day!")
