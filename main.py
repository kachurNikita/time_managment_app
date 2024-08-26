import datetime
import sqlite3
import os
from datetime import date
from time import strftime

# Get full date 
TODAY = date.today()

# Weekday by ID 
WEEKDAY = date.weekday(TODAY)

# Definition of 'Eisenhover_matrix class'
class EisenhoverMatrix:
    
    # def iterable_object(self,itterable_object):
    #     for i in itterable_object:
    #         return i 
    
    # Connection to sqlite database
    def sqlite_con(self, statement):
        conn = sqlite3.connect("EisenhoverMatrix.db")
        return self.statement_execution(conn, statement)

    # Function which will execute sqlite statements
    def statement_execution(self, conn, statement):
        cursor = conn.cursor()
        response = cursor.execute(statement)
        conn.commit()
        return response
        
    # Function wich allows us get a current time 
    def get_time(self):
        return strftime('%H')
        
    # Function which allows us to get day of the week 
    def get_weekday(self, day_id):
        response = self.sqlite_con(f"SELECT weekday FROM weekdays WHERE weekday_ID = '{day_id}'")
        return ''.join(response.fetchone())
    
    # Function which get quadrats for us 
    def get_quadrats(self, task_type):
        quadrats = self.sqlite_con(f"SELECT * FROM quadrat_importance").fetchall()
        if quadrats:
            return self.get_quardat_by_importance(quadrats, task_type)
        else: raise Exception('Qudarats are not exists')
        
    # Function which allows us to retrieve most important quadrat
    def get_quardat_by_importance(self, quadrats, task_type):
        for counter in range(4):
            from_list_to_dict = dict(quadrats)
            counter = str(counter)
            if counter in from_list_to_dict and self.is_quadrat_emtpy(from_list_to_dict[counter], task_type):
                return self.is_quadrat_emtpy(from_list_to_dict[counter], task_type)
    
    # Function which allows us to check  is quadrat empty ------>
    def is_quadrat_emtpy(self, quadrat_name, task_type):
        response = self.sqlite_con(f"SELECT task FROM '{quadrat_name}' WHERE task_group = '{task_type}'").fetchall()
        if response != []:
            return response
        return 
        
    # Function which alows us check what type of tasks to display based on day, time, and priority
    def get_task_type(self):
        if not self.is_today_weekend(self.return_day()) and self.is_job_time():
            return 'work'
        return 'personal'
        
    # Function which displays tasks
    def show_tasks(self):
        task_type = self.get_task_type()
        tasks_to_do = self.get_quadrats(task_type)
        return tasks_to_do
        
    # Function which allows us to check is there is a weekend
    def is_today_weekend(self, weekday):
        if  weekday.lower() == 'sunday' or weekday.lower() == 'saturday':
            return True
        return False
    
    # Function which allows us to check is it time for doing job or personal tasks
    def is_job_time(self):
        return int(self.get_time()) > 9 and int(self.get_time()) < 17
    
    # Function wich returns the weekday
    def return_day(self):
         weekday = self.sqlite_con(f"SELECT weekday FROM weekdays WHERE weekday_ID = '{WEEKDAY}'").fetchone()
         return ''.join(weekday)

    # Executes only ones and will create table for storing "qudrat importance" (have to be optimized )
    def create_quadrat_importance_table(self):  
        self.sqlite_con(f"CREATE TABLE quadrat_importance('importance', 'quadrat_name')")   
    
    # Function which allows us assign quadrat's importance
    def assign_quadrat_importance(self, importance, quadrat_name):
        self.sqlite_con(f'''INSERT INTO quadrat_importance('importance', 'quadrat_name') 
                        VALUES('{quadrat_name}', '{importance}')
                        ''')
    
    # Function which creates a weekdays table (have to be optimized ) 
    def create_weekdays_table(self):
        self.sqlite_con(f"CREATE TABLE weekdays('weekday_ID', 'weekday')")
    
    # Function which add weekdays and their id to database 
    def add_values_weekdays_table(self, weekdays):
        for key in weekdays:
            self.sqlite_con(f'''INSERT INTO weekdays('weekday_ID', 'weekday')
                            VALUES('{key}', '{str(weekdays[key])}')
                            ''')
            
    # Function which allows to check wheter quadrat with this name is exists, in order to prevent duplication (implement itteration)
    def is_quadrat_exist(self, quadrat_name):
        quadrat_exist = False
        quadrat_list_query = "SELECT name FROM sqlite_master WHERE type='table' ORDER BY Name"
        if self.sqlite_con(quadrat_list_query).fetchall():
            for quadrat in self.sqlite_con(quadrat_list_query).fetchall():
                if ''.join(quadrat) == quadrat_name:
                    quadrat_exist = not quadrat_exist
            else: return quadrat_exist
        else: return quadrat_exist
        
    # Function which allows to check how many tables (quadrats) at database (MAX 4 allowed) (implement itteration)
    def is_quadrats_limit(self):
        quadrat_counter = 0
        quadrat_list_query_response = self.sqlite_con("SELECT 'quadrat name' FROM quadrat_importance")
        for quadrat in quadrat_list_query_response.fetchall():
            quadrat_counter += 1
        return quadrat_counter < 4
    
    # Function which allows to check does task exist (implement itteration)
    def is_task_exist(self, quadrat_name, task):
        for i in self.sqlite_con(f"SELECT task FROM {quadrat_name}").fetchall():
            if ''.join(i).lower() == task.lower():
                return True
    
    # Function which allows create table (quadrat) at database (matrix) (have to be optimized )
    def create_quadrat(self, quadrat_name, importance):
        if  self.is_quadrats_limit():
            if not self.is_quadrat_exist(quadrat_name):
                self.sqlite_con(f"CREATE TABLE {quadrat_name}('task', 'task_group', 'date', 'weekday')")
                self.assign_quadrat_importance(quadrat_name, importance)
                print(f'Quadrat {quadrat_name} is successfully created!')
            else: raise Exception(f'Quadrat with name {quadrat_name} is already exist!')
        else: raise Exception(f'Max quadrats limit')
       
    # Function which allows delete table (quadrat) from database (matrix)  
    def delete_quadrat(self, quadrat_name):
        if self.is_quadrat_exist(quadrat_name):
            self.sqlite_con(f"DROP TABLE IF EXISTS {quadrat_name}")
            self.sqlite_con(f'''DELETE FROM quadrat_importance WHERE quadrat_name = "{quadrat_name}"''')
            print(f'Quadrat {quadrat_name} successfully deleted!')
        else: print(f'Quadrat with name {quadrat_name} is not exist!')
    
    # Function which allows add task to table's column (quadrat)
    def add_task(self, quadrat_name, task, task_type):
        if self.is_quadrat_exist(quadrat_name):
            if not self.is_task_exist(quadrat_name, task):
                self.sqlite_con(f'''
                                   INSERT INTO {quadrat_name}('task', 'task_group', 'date', 'weekday')
                                   VALUES('{task}', '{task_type}', '{TODAY}', '{self.return_day()}')
                                   ''')
                print('Values is added')
                return self.show_tasks()
            else: print(f'Task {task} is already exist!')
        else: raise Exception(f'Quadrat with name {quadrat_name} is not exist!')
        
    #  Function which allows us to delete task from quadrat (row from column in database)
    def delete_task(self, quadrat_name, task):
        if self.is_quadrat_exist(quadrat_name):
            if self.is_task_exist(quadrat_name, task):
                self.sqlite_con(f'''DELETE FROM {quadrat_name} WHERE task = "{task}"''')
                print(f"Task {task} successfully deleted!")
                self.show_tasks()
            else: raise Exception (f"Task {task} doesn't exist!")
        else: raise Exception(f'Quadrat with name {quadrat_name} is not exist!')
        
matrix = EisenhoverMatrix()
 
matrix.delete_quadrat('urgent')

# use weekdays api and in case if not work, use static from database
# Don't use Chatgpt if not working (set a limits)
# In order to response faster to  user regarding task, immidiatelly send request to CHATGPT API and create hidden block at HTML,
# Create additional database, in case ifsomething will wrong with current one 