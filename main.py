from matrix_quadrat import Quadrat
import datetime
import threading
import sqlite3
import os

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

    def is_quadrat_exist(self, quadrat_name):
        con = sqlite3.connect('eisenhover_matrix.db')
        cursor = con.cursor()
        quadrat_list_query = "SELECT name FROM sqlite_master WHERE type='table' ORDER BY Name"
        result = cursor.execute(quadrat_list_query)
        for quadrat in result.fetchall():
            return ''.join(quadrat) == quadrat_name
    
    # def is_quadrats_limit(self):
    #     quadrat_iterator = 0
    #     for key in self.matrix.keys():
    #         quadrat_iterator += 1
    #     return quadrat_iterator < 4

    def is_quadrats_limit(self):
        quadrat_counter = 0
        quadrat_list_query = "SELECT name FROM sqlite_master WHERE type='table' ORDER BY Name"
        sqlite_connection = sqlite3.connect("eisenhover_matrix.db")
        cursor = sqlite_connection.cursor()
        result = cursor.execute(quadrat_list_query)
        for quadrat in result.fetchall():
            quadrat_counter += 1
        return quadrat_counter > 4
    
    
    # def is_task_exist(self, quadrat_name, task, task_type):
    #     if self.is_quadrat_exist(quadrat_name):
    #         return task in self.matrix[quadrat_name][task_type]
    #     else: raise Exception(f"Quadrat {quadrat_name} is not exist")
    
    # def create_quadrat(self, quadrat_type):
    #     if self.is_quadrats_limit():
    #         if not self.is_quadrat_exist(quadrat_type):
    #             self.matrix[quadrat_type] = Quadrat().create_quadrat()
    #             return self.matrix
    #         else:
    #             raise Exception (f"The quadrat {quadrat_type} is already exist")
    #     else:
    #         raise Exception ("No more quadrats can be added")
    
    def create_quadrat(self, quadrat_name):
        if not self.is_quadrats_limit():
            if not self.is_quadrat_exist(quadrat_name):
                con = sqlite3.connect('eisenhover_matrix.db')
                cursor = con.cursor()
                try:
                    cursor.execute(f"CREATE TABLE {quadrat_name}(personal, work)")
                except sqlite3.OperationalError as e:
                    if 'already exists' in str(e):
                        print(f'Quadrat with name {quadrat_name} is alredy exists')
                    else:
                        print('Unexpected error occurred')
            raise Exception('Quadrat')
                
        
    # def delete_quadrat(self, quadrat_name):
    #     if self.is_quadrat_exist(quadrat_name):
    #         self.matrix.pop(quadrat_name)
    #     else:
    #         raise Exception (f"Quadrat {quadrat_name} is not exist")
        
    # def add_task(self, task, task_type, quadrat_name):
    #     if self.is_quadrat_exist(quadrat_name):
    #         if not self.is_task_exist(quadrat_name, task, task_type):
    #             self.matrix[quadrat_name][task_type].append(task)
    #             print(f"Task {task} added to {quadrat_name}")
    #         else:
    #             raise Exception("Same task is already exist in a quadrat!")
    #     else:
    #         raise Exception(f"Quadrat {quadrat_name} is not exist")
    
    # def delete_task(self, quadrat_name, task, task_type): 
    #     if self.is_task_exist(quadrat_name, task, task_type):
    #         self.matrix[quadrat_name][task_type].remove(task)
    #         print(f"Task {task} deleted")
    #     else:
    #         raise Exception (f"Task | {task} | doesn't exist")
        

matrix = EisenhoverMatrix()

matrix.create_quadrat('dsds')


