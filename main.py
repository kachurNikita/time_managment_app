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
        iterator = 0
        for key in self.matrix.keys():
            iterator += 1
        return iterator < 4

    def create_quadrat(self, quadrat_type):
        if self.is_quadrats_limit():
            if not self.is_quadrat_exist(quadrat_type):
                self.matrix[quadrat_type] = Quadrat()
            else:
                raise KeyError (f"The quadrat {quadrat_type} is already exist")
        else:
            raise Exception ('No more quadrats can be added')
    
    def delete_quadrat(self, quadrat_name):
        if self.is_quadrat_exist(quadrat_name):
            self.matrix.pop(quadrat_name)
        else:
            raise Exception (f"Quadrat {quadrat_name} is not exist")
    
    def add_task(self, quadrat_type, task_size)
        
        
matrix_1 = EisenhoverMatrix()
matrix_1.create_quadrat('green')

















    
    