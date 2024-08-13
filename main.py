import datetime
import sqlite3
import os
from datetime import date
from time import strftime

TODAY = date.today()
WEEKDAY = date.weekday(TODAY)
temporary_store = {}

# Definition of 'Eisenhover_matrix class'
class EisenhoverMatrix:
    
    
    # Function wich allows us make connection to sqlite3 database and specific commands execution 
    def sqlite_con(self, statement):
        con = sqlite3.connect("EisenhoverMatrix.db")
        cursor = con.cursor()
        response = cursor.execute(statement)
        con.commit()
        return response
    
    # Function wich allows us get a current time 
    def get_time(self):
        return strftime('%H:%M')
        
    # Function which allows us to get day of the week 
    def get_weekday(self, day_id):
        response = self.sqlite_con(f"SELECT weekday FROM weekdays WHERE weekday_ID = '{day_id}'")
        return ''.join(response.fetchone())
    
    def get_quadrats(self):
        quadrats = self.sqlite_con(f"SELECT * FROM quadrat_importance").fetchall()
        return self.get_top_quadrat(quadrats)
    
    # Function which allows us to retrieve the most important quadrat based on the time and the day!
    def get_top_quadrat(self, quadrats):
        quadrat_name, importance = quadrats[0]
        if len(quadrats) > 1:
            for quadrat in quadrats:
                if quadrat[1] < importance:
                    importance = quadrat[1]
                    quadrat_name = quadrat[0]
            quadrats.remove(quadrat)
            return quadrats
        else:
            quadrats.remove(quadrat)
            return quadrats

        #     return self.store_temporary_here(quadrats)
        #     # return quadrat_name
        # else:
        #     quadrats.remove(quadrat)
        #     return self.store_temporary_here(quadrats)
            # return quadrat_name
    
    # Testing fnction
    def store_temporary_here(self, quadrat_name, importance):
        temporary_store[quadrat_name] = importance
        print(temporary_store)
        return temporary_store

    # Function which allows us to check is there is a weekend
    def is_today_weekend(self, weekday):
        weekday = self.return_day(weekday).lower()
        if weekday  == 'sunday' or weekday == 'saturday':
            return True
        else:
            return False
    
    # #  Function which allows us to identify which task group to chose 
    # def task_group(self, is_today_weekend, importance, quadrats, quadrat_name):
    #     if is_today_weekend:
    #         result = self.sqlite_con(f"SELECT task FROM {quadrat_name} WHERE task_group = 'work'").fetchall()
    #         return result
        # else
# -------------------------------------------------------------------
    
    # Executes only ones and will create table for storing "qudrat importance" (have to be optimized )
    # def create_quadrat_importance_table(self):  
    #     self.sqlite_con(f"CREATE TABLE quadrat_importance('quadrat_name', 'importance')")   
    
    # Function which allows us assign quadrat's importance
    # def assign_quadrat_importance(self, quadrat_name, importance):
    #     self.sqlite_con(f'''INSERT INTO quadrat_importance('quadrat_name', 'importance') 
    #                     VALUES('{quadrat_name}', '{importance}')
    #                     ''')
    
    # Function which creates a weekdays table (have to be optimized ) 
    def create_weekdays_table(self):
        self.sqlite_con(f"CREATE TABLE weekdays('weekday_ID', 'weekday')")
    
    # Function which add weekdays and their id to database
    def add_values_weekdays_table(self, weekdays):
        for key in weekdays:
            self.sqlite_con(f'''INSERT INTO weekdays('weekday_ID', 'weekday')
                            VALUES('{key}', '{str(weekdays[key])}')
                            ''')
            
     # Function wich returns the weekday
    def return_day(self, day_id):
         weekday = self.sqlite_con(f"SELECT weekday FROM weekdays WHERE weekday_ID = '{day_id}'")
         return ''.join(weekday.fetchone())

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
        quadrat_list_query_response = self.sqlite_con("SELECT 'quadrat name' FROM quadrat_importance")
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
                self.sqlite_con(f"CREATE TABLE {quadrat_name}('task', 'task_group', 'date', 'weekday')")
                self.store_temporary_here(quadrat_name, importance)
                # self.assign_quadrat_importance(quadrat_name, importance)
                print(f'Quadrat {quadrat_name} is successfully created!')
            else:
                raise Exception(f'Quadrat with name {quadrat_name} is already exist!')
        else:
            raise Exception(f'Max quadrats limit')
            
    # Function which allows delete table (quadrat) from database (matrix)  
    def delete_quadrat(self, quadrat_name):
        if self.is_quadrat_exist(quadrat_name):
            self.sqlite_con(f"DROP TABLE IF EXISTS {quadrat_name}")
            self.sqlite_con(f'''DELETE FROM  quadrat_importance WHERE quadrat_name  = "{quadrat_name}"''')
            print(f'Quadrat {quadrat_name} successfully deleted!')
        else:
            print(f'Quadrat with name {quadrat_name} is not exist!')
    
    # Function which allows add task to table's column (quadrat)
    def add_task(self, quadrat_name, task, task_type):
        if self.is_quadrat_exist(quadrat_name):
            if not self.is_task_exist(quadrat_name, task):
                self.sqlite_con(f'''
                                   INSERT INTO {quadrat_name}('task', 'task_group', 'date', 'weekday')
                                   VALUES('{task}', '{task_type}', '{TODAY}', '{self.return_day(WEEKDAY)}')
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

# matrix.get_top_quadrat()
matrix.create_quadrat('urgent', 1)
# matrix.delete_quadrat('important')
# matrix.add_task('urgent', 'Call client ', 'work')
# print(matrix.get_quadrats())







# Make it work
#  Implement it !








# Instead of of tables limitation, do limitation at important table +
# Create function which will check if current quadrat is empty, it will go to another one until finds not empty 
# Create function is working time , returns true or false
# Create Function which will check is there is any tasks left from previous day, if yes, just substitute day 

# Get Quadrats  +
# Get most important quadrat - Create new function for sorting quadrats - received quadrats from and returning the top one +
# Store the rest of quadrats somewhere 
# Get current time 
# Get current day 
# Sort task by day
# Sort task by time 

# Get all quadrats
# Get the day, becasue if its weekend,