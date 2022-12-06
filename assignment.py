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
    
    