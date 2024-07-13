from matrix_quadrat import Quadrat
import datetime
import threading
import sqlite3
import os


# Definition of 'Eisenhover_matrix class'
# Eisenhover_matrix class

class EisenhoverMatrix:
    def __init__(self):
        self.matrix = {}
    
    # def is_matrix_exists(self, matrix_name):
    #     return os.path.exists(matrix_name)
    
    # def create_matrix(self, matrix_name):
    #     if not self.is_matrix_exists(matrix_name):
    #         sqlite_connection = sqlite3.connect(matrix_name)
    #     else:
    #         raise Exception(f'Matrix {matrix_name} is already exist')
    
    # def show_matrix(self):
    #     if self.is_matrix_empty():
    #         raise Exception (f"There are no quadrats in matrix")
    #     else:
    #         return self.matrix
        
    # def is_matrix_empty(self, matrix_name):
    #     sqlite_connection = sqlite3.connect(matrix_name)
    #     cursor = sqlite_connection.cursor()
    #     return cursor.execute('SELECT name FROM sqlite_schema WHERE type ="table" name NOT LIKE "sqlite_%"')
    
    # Function which allows to check wheter quadrat with this name is exists, in order to prevent duplication 
    def is_quadrat_exist(self, quadrat_name):
        quadrat_exist = False
        con = sqlite3.connect("eisenhover_matrix.db")
        cursor = con.cursor()
        quadrat_list_query = "SELECT name FROM sqlite_master WHERE type='table' ORDER BY Name"
        if cursor.execute(quadrat_list_query).fetchall():
            for i in cursor.execute(quadrat_list_query).fetchall():
                if ''.join(i) == quadrat_name:
                    quadrat_exist = not quadrat_exist
            return quadrat_exist
        else:
            return quadrat_exist
        
    # Function which allows to check how many tables (quadrats) at database (MAX 4 allowed)
    def is_quadrats_limit(self):
        quadrat_counter = 0
        quadrat_list_query = "SELECT name FROM sqlite_master WHERE type='table' ORDER BY Name"
        sqlite_connection = sqlite3.connect("eisenhover_matrix.db")
        cursor = sqlite_connection.cursor()
        result = cursor.execute(quadrat_list_query)
        for quadrat in result.fetchall():
            quadrat_counter += 1
        return quadrat_counter < 4

    def is_task_exist(self, quadrat_name, task):
        sqlite_connection = sqlite3.connect("eisenhover_matrix.db")
        cursor = sqlite_connection.cursor()
        reslt = cursor.execute(f"SELECT task FROM {quadrat_name}")
        for i in reslt.fetchall():
            if ''.join(i).lower() == task.lower():
                return True
    
    # Function which allows create table (quadrat) at database (matrix)
    def create_quadrat(self, quadrat_name):
        if  self.is_quadrats_limit():
            if not self.is_quadrat_exist(quadrat_name):
                con = sqlite3.connect('eisenhover_matrix.db')
                cursor = con.cursor()
                cursor.execute(f"CREATE TABLE {quadrat_name} ('task', 'group')")
                print(f'table {quadrat_name} is successfully created!')
            else:
                raise Exception(f'Quadrat with name {quadrat_name} is already exist!')
        else:
            raise Exception(f'Max quadrats limit')
        
    # Function which allows delete table (quadrat) from database (matrix)  
    def delete_quadrat(self, quadrat_name):
        if self.is_quadrat_exist(quadrat_name):
            con = sqlite3.connect('eisenhover_matrix.db')
            cursor = con.cursor()
            cursor.execute(f"DROP TABLE IF EXISTS {quadrat_name}")
            print(f'Quadrat {quadrat_name} successfully deleted!')
        else:
            print(f'Quadrat with name {quadrat_name} is not exist!')
    
    # Function which allows add task to table's column (quadrat)
    def add_task(self, quadrat_name, task, task_type):
        if self.is_quadrat_exist(quadrat_name):
            if not self.is_task_exist(quadrat_name, task):
                    con = sqlite3.connect('eisenhover_matrix.db')
                    cursor = con.cursor()
                    cursor.execute(f''' INSERT INTO {quadrat_name}('task', 'group') VALUES('{task}', '{task_type}')''')
                    con.commit()
                    print('Values is added')
            else:
                print(f'Task {task} is already exist!')
        else:
            raise Exception(f'Quadrat with name {quadrat_name} is not exist!')
    #  Function which allows us to delete task from quadrat (row from column in database)
    def delete_task(self, quadrat_name, task):
        if self.is_quadrat_exist(quadrat_name):
            if self.is_task_exist(quadrat_name, task):
                con = sqlite3.connect('eisenhover_matrix.db')
                cursor = con.cursor()
                cursor.execute(f'''DELETE FROM {quadrat_name} WHERE task = "{task}" ''')
                con.commit()
                print(f"Task {task} successfully deleted!")
            else:
                raise Exception (f"Task {task} doesn't exist!")
        else:
            raise Exception(f'Quadrat with name {quadrat_name} is not exist!')

matrix = EisenhoverMatrix()

# matrix.create_quadrat('main')
# matrix.add_task('main', 'sport', 'personal')
# matrix.add_task('main', 'jiujitsu', 'personal')
# matrix.add_task('main', 'Call to ', 'work')
# matrix.delete_quadrat('main')
matrix.delete_task('main', 'sport')


# Work on add_task function - 1. check if quadrat exist 2. check if the task exists
# Work on delete_task function, check wheter quadrat and task are exists 

# Implement  to one function where connection to sqlite 




