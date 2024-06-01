import datetime
import threading

# 1 create a function for adding tasks to my matrix +
# Create function protection, create testing for the function
# Create function for deleting task, createfunction protection, create testing for function
# Create preventing dublication function, which will ask me before adding element to list, do i really want to add this task?
# Create function protection, testing for  the function 
# Create function which will switching tasks (when it is break)

# work_time = '5:00 PM'
eisenhower_matrix_1 = {
    'green': {
        'work': {
            'small': ['Job fair case notes', 'computer literacy'],
            'medium': {'Create resumefor the client'},
            'large': {'Enroll client process'},
        },
        'personal': {
            'small': ['Register at "Rover"'],
            'medium': ['Make PSEG payment'],
            'large': ['Call to USCIS'],
        }
    }
}

# Function for adding task to specific quadrant and task  type
# def add_task_to_matrix(task: str, task_importance: str, task_size: str, task_type: str):
#     eisenhower_matrix_1[task_importance][task_type][task_size].append(task)
#     print('Task successfully added!')
#     print(eisenhower_matrix_1)
    

# add_task_to_matrix('lol', 'green', 'small', 'personal')




# Eisenhover_matrix class


class EisenhoverMatrix:
    def __init__(self):
        self.matrix = {}
    
    # def add_task_to_quadrat(self, task, task_importance, task_size, task_type):
    #     self.matrix[task_importance][task_type][task_size].append(task)
    #     print(self.matrix)
                
    def show_matrix(self):
        print(self.matrix)
        
    def is_quadrat_exist(self, quadrat):
        return quadrat in self.matrix.keys()

    def create_quadrat(self, quadrat_name):
        if not self.is_quadrat_exist(quadrat_name):
            self.matrix[quadrat_name] = {}
        else:
            raise KeyError (f"The quadrat {quadrat_name} is already exist")
    
    def delete_quadrat(self, quadrat_name):
        if self.is_quadrat_exist(quadrat_name):
            self.matrix.pop(quadrat_name)
        else:
            raise Exception (f'Quadrat {quadrat_name} is no longer exist')

            
        
instance = EisenhoverMatrix()

instance.create_quadrat('green')
instance.create_quadrat('blue')
instance.show_matrix()
instance.delete_quadrat('blue')
instance.show_matrix()
instance.create_quadrat('green')





    
    