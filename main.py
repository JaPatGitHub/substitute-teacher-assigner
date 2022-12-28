import sys
import sqlsimp as sql
import datesimp as date


def check_list(tt_pylist, list_pylist):
    
    teachers = []
    not_found = []
    
    for i in range(1, len(list_pylist)):
        teacher = list_pylist[i][1].lower()
        teachers.append(teacher)
        
    for i in range(1, len(tt_pylist)):
        for j in range(1, len(tt_pylist[i])):
            if tt_pylist[i][j].lower() in teachers:
                continue
            else:
                if tt_pylist[i][j] not in not_found:
                    not_found.append(tt_pylist[i][j])
                
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
    
    print(absent_no, type(absent_no))
    absentees = []
    for e in absent_no:
        absentees.append(teachers_list[e][1])
    
    return absentees

def tt_func_details(tt):
    count = 0
    teachers_asg = {} # periods the teachers are already assigned
    period_load = {} # teachers having a particular no. of periods

    for i in range(1, len(tt)):
        for j in range(1, len(tt[i])):
            period = j
            teacher = tt[i][j]
            
            if tt[i][j] == None:
                count += 1
                continue

            elif teacher in teachers_asg.keys():
                teachers_asg.append(period)

                new_load = len(teachers_asg[teacher])
                old_load = new_load - 1

                period_load[old_load].pop(teacher)
                period_load[new_load].append(teacher)
                
            else:
                teachers_asg.append(period)
                period_load[1].append(teacher)  
                
    return teachers_asg, period_load, count

"""
def find_period_load(tt):
    teachers = {}
    period_load = {}

    for i in range(1, len(tt)):
        for j in range(1, len(tt[i])):
            teacher = tt[i][j]

            if teacher == None:
                continue

            elif teacher in teachers.keys():
                old_load = teachers[teacher]
                new_load = old_load + 1

                teachers[teacher] = new_load
                period_load[old_load].pop(teacher)
                period_load[new_load].append(teacher)
                
            else:
                teachers[teacher] = 1
                period_load[i].append(teacher)

    return period_load
"""
    
def find_subst_pool(period_load, num_subst):
    subst_teachers = []
    count = 0
    subst_pool = {}
    periods = list(period_load.keys())
    periods.sort()

    for e in periods:
        if count > num_subst:
            break
        else:
            subst_pool[e] = period_load[e]
            subst_teachers.extend(e)
            count += len(subst_teachers)

    return subst_pool



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

for e in tt_std:
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
        sql.drop_table(teachers_table)
        
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

# modify this to details: num_subst = count_subst_periods(tt_func)
