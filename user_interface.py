from flask import Flask, render_template, request, url_for, g
from apscheduler.schedulers.background import BackgroundScheduler
from chat_gtp_API import chat_gpt_response
from main import EisenhoverMatrix
from markupsafe import escape


app = Flask(__name__)

@app.route('/')
@app.route('/<explanation>')
def index(explanation = None):
    return render_template('index.html', tasks=check_tasks_hourly())

# -------
def check_tasks_hourly(): 
        return matrix.show_tasks()
    

# Backgroundscheduler instance
scheduler = BackgroundScheduler()

# EisenhoverMatrix instance
matrix = EisenhoverMatrix()

# Each hour function will be executed in order to check current time and based on it show tasks to do
scheduler.add_job(check_tasks_hourly, 'interval', minutes=60)

# starts scheduler instance
scheduler.start()

