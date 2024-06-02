import datetime
import threading

# Eisenhover_matrix class

class EisenhoverMatrix:
    def __init__(self):
        self.matrix = {}
            
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






    
    