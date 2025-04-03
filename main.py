from chat_gtp_API import chat_gpt_response
from datetime import date
from time import strftime
import tempfile
import datetime
import sqlite3
import os

# Get full date 
TODAY = date.today()

# Weekday by ID 
WEEKDAY = date.weekday(TODAY)

# Definition of 'Eisenhover_matrix class'
class EisenhoverMatrix:
        
    # Connection to sqlite database
    def sqlite_con(self, statement, data = None):
        conn = sqlite3.connect("EisenhoverMatrix.db")
        if data:
            return self.statement_execution(conn, statement, data)
        else: 
            return self.statement_execution(conn, statement)

    # Function which will execute sqlite statements
    def statement_execution(self, conn, statement, data = None):
        cursor = conn.cursor()
        if data:
            response = cursor.execute(statement, data)
            conn.commit()
            return response
        else: 
            response = cursor.execute(statement)
            conn.commit()
            return response
        
    # Function wich allows us get a current time 
    def get_time(self):
        return strftime('%H')
        
    # Function which allows us to get day of the week 
    def get_weekday(self, day_id):
        response = self.sqlite_con(f'''
                                   SELECT weekday FROM weekdays WHERE weekday_ID = "{day_id}"
                                   ''')
        return ''.join(response.fetchone())
    
    # Function which get quadrats for us 
    def get_quadrats(self, task_type):
        quadrats = self.sqlite_con(f'''SELECT * FROM quadrat_importance''').fetchall()
        if quadrats:
            return self.get_quardat_by_importance(quadrats, task_type)
        else: raise Exception('Qudarats are not exists')
        
    # Function which allows us to retrieve most important quadrat
    def get_quardat_by_importance(self, quadrats, task_type):
        for counter in range(1, 5):
            from_list_to_dict = dict(quadrats)
            counter = str(counter)
            if counter in from_list_to_dict and self.is_quadrat_emtpy(from_list_to_dict[counter], task_type):
                return self.is_quadrat_emtpy(from_list_to_dict[counter], task_type)
    
    # Function which allows us to check is quadrat empty ------>
    def is_quadrat_emtpy(self, quadrat_name, task_type):
        response = self.sqlite_con(f'''
                                   SELECT task, task_breakdown FROM '{quadrat_name}' WHERE task_group = "{task_type}"
                                   ''').fetchall()
        if response != []:
            return [response,  quadrat_name]
        
    # Function which alows us check what type of tasks to display based on day, time, and priority
    def get_task_type(self):
        if  not self.is_today_weekend(self.return_day()) and self.is_job_time():
            return 'work'
        else:
            return 'personal'
            
    # Function which displays current tasks
    def show_current_tasks(self):
        task_type = self.get_task_type()
        current_tasks = self.get_quadrats(task_type)
        tasks = self.show_tasks()
        return [current_tasks, tasks]
    
    # Function which allows us to display all tasks
    def show_tasks(self):
        return self.sqlite_con('''
                        SELECT * FROM TASKS''').fetchall()
        
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
         weekday = self.sqlite_con(f'''
                                   SELECT weekday FROM weekdays WHERE weekday_ID = "{WEEKDAY}"
                                   ''').fetchone()
         return ''.join(weekday)

    # Executes only ones and will create table for storing "qudrat importance" (have to be optimized )
    def create_quadrat_importance_table(self):  
        self.sqlite_con(f'''
                        CREATE TABLE quadrat_importance('importance', 'quadrat_name')
                        ''')   
    
    # Function which allows us assign quadrat's importance
    def assign_quadrat_importance(self, importance, quadrat_name):
        self.sqlite_con(f'''INSERT INTO quadrat_importance('importance', 'quadrat_name') 
                        VALUES('{quadrat_name}', '{importance}')
                        ''')
    
    # Function which creates a weekdays table (have to be optimized ) 
    def create_weekdays_table(self):
        self.sqlite_con(f'''
                        CREATE TABLE weekdays('weekday_ID', 'weekday')
                        ''')
    
    # Function which add weekdays and their id to database 
    def add_values_weekdays_table(self, weekdays):
        for key in weekdays:
            self.sqlite_con(f'''INSERT INTO weekdays('weekday_ID', 'weekday')
                            VALUES('{key}', '{str(weekdays[key])}')
                            ''')
            
    # Function which allows to check wheter quadrat with this name is exists, in order to prevent duplication (implement itteration)
    def is_quadrat_exist(self, quadrat_name):
        quadrat_exist = False
        quadrat_list_query = '''SELECT name FROM sqlite_master WHERE type='table' ORDER BY Name'''
        if self.sqlite_con(quadrat_list_query).fetchall():
            for quadrat in self.sqlite_con(quadrat_list_query).fetchall():
                if ''.join(quadrat) == quadrat_name:
                    quadrat_exist = not quadrat_exist
            else: return quadrat_exist
        else: return quadrat_exist
        
    # Function which allows to check how many tables (quadrats) at database (MAX 4 allowed) (implement itteration)
    def is_quadrats_limit(self):
        quadrat_counter = 0
        quadrat_list_query_response = self.sqlite_con('''
                                                      SELECT 'quadrat name' FROM quadrat_importance
                                                      ''')
        for quadrat in quadrat_list_query_response.fetchall():
            quadrat_counter += 1
        return quadrat_counter < 4
    
    # Function which allows to check does task exist (implement itteration)
    def is_task_exist(self, quadrat_name, task):
        for i in self.sqlite_con(f'''
                                    SELECT task FROM "{quadrat_name}"
                                 ''').fetchall():
            if ''.join(i).lower() == task.lower():
                return True
    
    # Function which allows create table (quadrat) at database (matrix) (have to be optimized )    
    def create_quadrat(self, quadrat_name, importance):
        if  self.is_quadrats_limit():
            if not self.is_quadrat_exist(quadrat_name):
                self.sqlite_con(f'''CREATE TABLE '{quadrat_name}' (
                        task TEXT NOT NULL,
                        task_breakdown TEXT NOT NULL,
                        task_group TEXT NOT NULL,
                        date TEXT NOT NULL,
                        weekday TEXT NOT NULL
                        )
                    ''')
                self.assign_quadrat_importance(quadrat_name, importance)
                print(f'Quadrat {quadrat_name} is successfully created!')
            else: raise Exception(f'Quadrat with name {quadrat_name} is already exist!')
        else: raise Exception(f'Max quadrats limit')
       
    # Function which allows delete table (quadrat) from database (matrix)  
    def delete_quadrat(self, quadrat_name):
        if self.is_quadrat_exist(quadrat_name):
            self.sqlite_con(f'''
                                DROP TABLE IF EXISTS "{quadrat_name}"
                            ''')
            self.sqlite_con(f'''
                            DELETE FROM quadrat_importance WHERE quadrat_name = "{quadrat_name}"
                            ''')
            print(f'Quadrat {quadrat_name} successfully deleted!')
        else: print(f'Quadrat with name {quadrat_name} is not exist!')
    
    # Function which allows add task to table's column (quadrat)
    def add_task(self, quadrat_name, task, task_type):
        if self.is_quadrat_exist(quadrat_name):
            if not self.is_task_exist(quadrat_name, task):
                breakdown_problem = chat_gpt_response(task)
                data = (task, breakdown_problem, task_type, TODAY, self.return_day())
                self.add_task_to_pool(task, breakdown_problem)
                self.sqlite_con(f'''
                                   INSERT INTO "{quadrat_name}"('task', 'task_breakdown', 'task_group', 'date', 'weekday')
                                   VALUES(?, ?, ?, ?, ?)
                                   ''', data)
                print('Values is added')
            else: print(f'Task {task} is already exist!')
        else: raise Exception(f'Quadrat with name {quadrat_name} is not exist!')
    
    # Function wich allows us add task to to pool of tasks 
    def add_task_to_pool(self, task, breakdown_problem):
        self.sqlite_con(f'''INSERT INTO TASKS('task', 'breakdown_problem') VALUES(?, ?)''', (task, breakdown_problem))
                               
    #  Function which allows us to delete task from quadrat (row from column in database)
    def delete_task(self, quadrat_name, task):
        if self.is_quadrat_exist(quadrat_name):
            if self.is_task_exist(quadrat_name, task):
                self.sqlite_con(f'''
                                    DELETE FROM "{quadrat_name}" WHERE task = "{task}"
                                ''')
                print(f"Task {task} successfully deleted!")
            else: raise Exception (f"Task {task} doesn't exist!")
        else: raise Exception(f'Quadrat with name {quadrat_name} is not exist!')
        

matrix = EisenhoverMatrix()
# matrix.delete_quadrat()
# matrix.add_task_to_pool('Ride bycicle', 'lololo')


# delete task function
# display all availiable tasks besides other column (create newtable with all tasks and retrieve data from there)
# prevent user submit tasks without provided parameters


# Make function of deleting tasks fro page
# Make function for adding tasks from page
# Create function which will display all tasks work and personal and from allquadrats 


# Create function, which will get all tasks and will display them to the user:
# 1. create table, which will store all task, just one columnt task
# 2. And  just simply retrieve this task from table and return it,  together with quadrat_name and tasks
# 3. Create function, which will delete task from this table as
# Maybe at the moment when task added, add it to other table, in order to easyaly get them and display
# make uinit tests
# use weekdays api and in case if not work, use static from database
# Don't use Chatgpt if not working (set a limits)
# Create additional database, in case if something will wrong with current one 
