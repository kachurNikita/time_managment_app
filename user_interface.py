from flask import Flask
from markupsafe import escape
from main import EisenhoverMatrix
from flask import render_template, request, url_for
from chat_api_test import ai_response

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        task = request.form.get('btn')
        sub_task = ai_response(task)
        return problem_breakdown(sub_task)
    return render_template('index.html', tasks=matrix.show_tasks())


def problem_breakdown(sub_task):
        return f'<p>{sub_task}</p>'

matrix = EisenhoverMatrix()


# Create main page, with options to choose: create quadrat, add task, display tasks