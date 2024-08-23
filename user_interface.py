from flask import Flask
from markupsafe import escape
from main import EisenhoverMatrix
from flask import render_template, request, url_for

app = Flask(__name__)


# Create quadrat page 
@app.route('/quadrats', methods=['GET', 'POST'])
def create_quadrat():
    if  request.method == 'POST':
        quadrat_name = request.form.get('quadrat')
        importance = request.form.get('importance')
        if quadrat_name and importance:
            matrix.create_quadrat(escape(quadrat_name), int(escape(importance)))
    return render_template('create_quadrat.html')

#  Main page functions 
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        quadrat = request.form.get('quadrat')
        task = request.form.get('task')
        if quadrat == 'quadrat':
            return create_quadrat()
        else: return add_task()
    return render_template('index.html')

# Add task page
@app.route('/add_task', methods=['GET', 'POST'])
def add_task():
    if  request.method == 'POST':
        quadrat_name = request.form.get('quadrat_name')
        task = request.form.get('task')
        task_type = request.form.get('task_type')
    return render_template('add_task.html')


@app.route('/display_tasks', methods =['GET', 'POST'])
def display_tasks():
    test = 'Passing parameter works'
    return render_template('display_task.html', test=test)
    
matrix = EisenhoverMatrix()

# @app.route('/nik')
# def display_it


# Create main page, with options to choose: create quadrat, add task, display tasks