import datetime
import threading
import sqlite3
import os
# import pandas as pd

from datetime import date

# name = ['John', 'Mary', 'Sherlock']
# age = [11, 12, 13]
# df = pd.DataFrame({ 'Name': name, 'Age': age })
# df.index.name = 'ID'

# df.to_excel('spreadsheet.xlsx')

today = date.today()
weekday = date.weekday(today)

# Definition of 'Eisenhover_matrix class'
class EisenhoverMatrix:
    def __init__(self):
        self.matrix = {}
    
    # Function wich allows us make connection to sqlite3 database and specific commands execution 
    def sqlite_con(self, statement):
        con = sqlite3.connect("EisenhoverMatrix.db")
        cursor = con.cursor()
        result = cursor.execute(statement)
        con.commit()
        return result
    
    
    # Executes only ones and will create table for storing "qudrat importance" (have to be optimized )
    def create_quadrat_importance_table(self):  
        self.sqlite_con(f"CREATE TABLE quadrat_importance('quadrat name', 'quadrat importance')")   
    
    # Function which allows us assign quadrat's importance
    def assign_quadrat_importance(self, quadrat_name, importance):
        self.sqlite_con(f'''INSERT INTO quadrat_importance('quadrat name', 'quadrat importance') 
                        VALUES('{quadrat_name}', '{importance}')
                        ''')
    
    # Function which creates a weekdays table (have to be optimized ) 
    def create_weekdays_table(self):
        self.sqlite_con(f"CREATE TABLE weekdays('weekday ID', 'weekday')")
    
    # Function which add weekdays and their id to database
    def add_values_weekdays_table(self, weekdays):
        for key in weekdays:
            self.sqlite_con(f'''INSERT INTO weekdays('weekday ID', 'weekday')
                            VALUES('{key}', '{str(weekdays[key])}')
                            ''')
        
     # Function wich returns the weekday
    def return_day(self, day):
         return self.sqlite_con(f"SELECT weekday FROM weekdays WHERE weekday ID ='{day}'")
         
    # Function which allows to check wheter quadrat with this name is exists, in order to prevent duplication 
    def is_quadrat_exist(self, quadrat_name):
        quadrat_exist = False
        quadrat_list_query = "SELECT name FROM sqlite_master WHERE type='table' ORDER BY Name"
        if self.sqlite_con(quadrat_list_query).fetchall():
            for i in self.sqlite_con(quadrat_list_query).fetchall():
                if ''.join(i) == quadrat_name:
                    quadrat_exist = not quadrat_exist
            else:
                return quadrat_exist
        else:
            return quadrat_exist
        
    # Function which allows to check how many tables (quadrats) at database (MAX 4 allowed)
    def is_quadrats_limit(self):
        quadrat_counter = 0
        quadrat_list_query = "SELECT name FROM sqlite_master WHERE type='table' ORDER BY Name"
        quadrat_list_query_response = self.sqlite_con(quadrat_list_query)
        for quadrat in quadrat_list_query_response.fetchall():
            quadrat_counter += 1
        return quadrat_counter < 4
    
    # Function which allows to check does task exist
    def is_task_exist(self, quadrat_name, task):
        for i in self.sqlite_con(f"SELECT task FROM {quadrat_name}").fetchall():
            if ''.join(i).lower() == task.lower():
                return True
    
    # Function which allows create table (quadrat) at database (matrix) (have to be optimized )
    def create_quadrat(self, quadrat_name, importance):
        if  self.is_quadrats_limit():
            if not self.is_quadrat_exist(quadrat_name):
                self.sqlite_con(f"CREATE TABLE {quadrat_name}('task', 'group', 'date', 'weekday')")
                self.assign_quadrat_importance(quadrat_name, importance)
                print(f'Quadrat {quadrat_name} is successfully created!')
            else:
                raise Exception(f'Quadrat with name {quadrat_name} is already exist!')
        else:
            raise Exception(f'Max quadrats limit')
            
    # Function which allows delete table (quadrat) from database (matrix)  
    def delete_quadrat(self, quadrat_name):
        if self.is_quadrat_exist(quadrat_name):
            self.sqlite_con(f"DROP TABLE IF EXISTS {quadrat_name}")
            self.sqlite_con(f'''DELETE FROM  quadrat_importance WHERE "quadrat name"  = "{quadrat_name}"''')
            print(f'Quadrat {quadrat_name} successfully deleted!')
        else:
            print(f'Quadrat with name {quadrat_name} is not exist!')
    
    # Function which allows add task to table's column (quadrat)
    def add_task(self, quadrat_name, task, task_type):
        if self.is_quadrat_exist(quadrat_name):
            if not self.is_task_exist(quadrat_name, task):
                self.sqlite_con(f'''
                                   INSERT INTO {quadrat_name}('task', 'group', 'date', 'weekday')
                                   VALUES('{task}', '{task_type}', '{today}', '{self.return_day(date.weekday(today))}')
                                   ''')
                print('Values is added')
            else:
                print(f'Task {task} is already exist!')
        else:
            raise Exception(f'Quadrat with name {quadrat_name} is not exist!')
        
    #  Function which allows us to delete task from quadrat (row from column in database)
    def delete_task(self, quadrat_name, task):
        if self.is_quadrat_exist(quadrat_name):
            if self.is_task_exist(quadrat_name, task):
                self.sqlite_con(f'''DELETE FROM {quadrat_name} WHERE task = "{task}"''')
                print(f"Task {task} successfully deleted!")
            else:
                raise Exception (f"Task {task} doesn't exist!")
        else:
            raise Exception(f'Quadrat with name {quadrat_name} is not exist!')
        
        
matrix = EisenhoverMatrix()
# matrix.create_weekdays_table()
# matrix.add_values_weekdays_table(weekdays)
# matrix.delete_quadrat('quadrat_importance')
# matrix.create_quadrat_importance_table()
        
# matrix.create_quadrat('important', 1)
# matrix.add_task('test', 'sport', 'personal')
matrix.delete_quadrat('important')


# Create function - for optimization where i see that commands repeats (break down sqlite_con function: 1. specificaly for sqlite connections, func for commands, such as: create table and Insert into)





# Create function which will display to me what i have to do at the current moment
# if i don't have any quadrats it will tell me to create one 
#  if it is only one quadrat  task will be added there and i have to choose button (work or personal)
# It identify day and also it identify time 
#  if it is a Weekends work task will not be displayed 


# Have a window with input: ADD TASK and after task specification give quadrat name if none exists 
# Function add task where i can just simply write the task, and it will ask at which quadrat i want add this task,
# if there are no quadrats, will call function create quadrate and will add this task to the database
# Store somewhere acomplished tasks 
# Right now one of mine main goals is display tasks based on the day and time period

# At each launch, program have to check wheter it is something left from previous day, if yes, schedule it for today
# Detect current timeof opening and based on  time display the tasks or task
# For UA / maybe have a task and display task and at the right side make a window in order to break down the problem if it dificult to start

# Create function display task:
# Identify day
# identify current time 
# identify the table which is exists (green, yeelow, blue, red) - green (urgent-important) - make 
# When creating table, create separate database in order to 



# Acomplished tasks  
# Create column at database which stands for the date and time +
# Also i have to track weekday and probably add it to database as well in order +
# Adjust functionality  for sqlite connection, becasue to much code becasue of it +
# create seperate database for storing my default values such as: quadrats importance and weekdays +
