import mysql.connector as sqltor
import csv

con = None
cur = None

def connect_sql():
    global con
    global cur
    con = sqltor.connect(host="localhost", user="root", password="YES", charset = "utf8")
    cur = con.cursor()
    
def disconnect_sql():
    con.close()
    
def use_db(db_name):
    cur.execute("use {0}".format(db_name))
    
def create_table(table_name, header_list, header_parameters):
   
    if len(header_list) != len (header_parameters):
        raise Exception("header_list and header_parameters inconsistent")
        
    else:
        qry = "Create table {0}(".format(table_name)
        
        for i in range(len(header_list)):
            # For all except last index
            if i != (len(header_list) - 1):
                qry += "{0} {1}, ".format(header_list[i], header_parameters[i])          
            # Last index
            else:
                qry += "{0} {1});".format(header_list[i], header_parameters[i])
                
        cur.execute(qry)
        
def drop_table(table_name):
    qry = "drop table {0};".format(table_name)
    cur.execute(qry)
            
def insert_values(table_name, value_list):
    qry = "insert into {0} values(".format(table_name)
    
    for i in range(len(value_list)):
        # For all except last index
        if i != (len(value_list) - 1):
            qry += "'{0}', ".format(value_list[i])          
        # Last index
        else:
            qry += "'{0}');".format(value_list[i])
            
    cur.execute(qry)
    con.commit()
    
def read_table(table_name):
    
    qry = "desc {0}".format(table_name)
    cur.execute(qry)
    desc = cur.fetchall()
    
    header = []
    for e in desc:
        header.append(e[0])
    
    qry = "select * from {0}".format(table_name)
    cur.execute(qry)
    data = cur.fetchall()
    
    data = [header] + data
    return data

def nullify_val(table_name, values_list):
    columns = read_table(table_name)[0]
    
    for e in columns:
        for f in values_list:
            qry = "update {0} modify update set {1} = null where {1} = '{2}';".format(table_name, e, f)
            cur.execut(qry)
            con.commit()
            
def modify_val(table_name, target_column, target_value, reference_column, reference_value):
    #table_list = read_table(table_name)
    
    qry = "update {0} modify set {1} = '{2}' where {3} = '{4}'".format(table_name, target_column, target_value, reference_column, reference_value)
    cur.execute(qry)
    con.commit()
    
def csv_to_sql(csv_file, table_name):
    global con
    global cur
    
    with open(csv_file, "r") as f:
        reader = csv.reader(f)
        L = list(reader)
        
    for i in range(len(L)):
        if L[i] == []:
            L.delete(L[i])
    
    header_list = []
    header_parameters = []
    
    for i in range(len(L[0])):
        header_list.append(L[0][i])
        
        try:
            for j in range(1, len(L)):
                is_int = int(L[j][i])    
            header_parameters.append("int")
                
        except:
            header_parameters.append("varchar(50)")

    create_table(table_name, header_list, header_parameters)
    
    for i in range(1, len(L)):
        insert_values(table_name, L[i])
    
            
                
                
            