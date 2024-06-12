from matrix_quadrat import Quadrat
import datetime
import threading

# Eisenhover_matrix class

class EisenhoverMatrix:
    def __init__(self):
        self.matrix = {}
       
    def show_matrix(self):
        if self.is_matrix_empty():
            raise Exception (f'There are no quadrats in matrix')
        else:
            return self.matrix
        
    def is_matrix_empty(self):
        return self.matrix == {}
    
    def is_quadrat_exist(self, quadrat):
        return quadrat in self.matrix.keys()
    
    def is_quadrats_limit(self):
        quadrat_iterator = 0
        for key in self.matrix.keys():
            quadrat_iterator += 1
        return quadrat_iterator < 4
    
    def is_task_exist(self, quadrat_name, task, task_type, task_size):
        if self.is_quadrat_exist(quadrat_name):
            return task in self.matrix[quadrat_name][task_type][task_size]
        else: raise Exception(f"Quadrat {quadrat_name} is not exist")
    
    def create_quadrat(self, quadrat_type):
        if self.is_quadrats_limit():
            if not self.is_quadrat_exist(quadrat_type):
                self.matrix[quadrat_type] = Quadrat().create_quadrat()
            else:
                raise KeyError (f"The quadrat {quadrat_type} is already exist")
        else:
            raise Exception ('No more quadrats can be added')
        
    def delete_quadrat(self, quadrat_name):
        if self.is_quadrat_exist(quadrat_name):
            self.matrix.pop(quadrat_name)
        else:
            raise Exception (f"Quadrat {quadrat_name} is not exist")
        
    def add_task(self, task, task_size, task_type, quadrat):
        if self.is_quadrat_exist(quadrat):
            self.matrix[quadrat][task_type][task_size].append(task)
            return self.matrix
    
    def delete_task(self, quadrat_name, task, task_type, task_size): 
        if self.is_task_exist(quadrat_name, task, task_type, task_size):
            self.matrix[quadrat_name][task_type][task_size].remove(task)
        else:
            raise Exception (f"Task |-{task}-| doesn't exist")
        

    
eisenhover_matrix = EisenhoverMatrix()
eisenhover_matrix.create_quadrat('urgent_important')
eisenhover_matrix.add_task('Do laundry', 'medium', 'personal', 'urgent_important')

print(eisenhover_matrix.show_matrix())
print(eisenhover_matrix.delete_task('urgent_important', 'Do sport', 'personal', 'medium'))




    
    