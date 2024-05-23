import datetime
import threading

# Create data structure than can store my tasks +
# Receive current time and date 
# Show up time/ show up all  stored tasks 
# make a simple prioritazation by assigning number for each task. Taslk with number closer to 0 is more priority. 

# simple structure which acts as a "database"

eisenhower_matrix = {
    'green': ['do task that Mahamat said until Friday (included)', 'Send job fair invitation and make notes about it',
              'Create Ukrainian chat group'],
    'yellow': ['Do Jiu Jitsu', 'Learn data analyst course', 'Do breathing exercise', 'Apply for jobs', 'Register at "Rover",'
               'find additional income', 'pay bills'],
    'blue':  ['Wash clothes', 'clean apartment', 'make food',],
    'red': []
}

print(eisenhower_matrix['green'])