from flask import Flask, render_template, request, redirect, flash, url_for, session, g
from users import verify_user, register_user, get_user_by_id
from main import EisenhoverMatrix
from chat_gtp_API import chat_gpt_response

app = Flask(__name__)
app.secret_key = '4b7c3a2b8c9e1d4f7e6a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3d4e5f6a7b8c9d0e'

@app.route('/')
def home():
    return redirect('/login')


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user_id = verify_user(username, password)

        if user_id:
            session["user_id"] = user_id 
            flash("Login successful!", "success")
            return redirect("/dashboard")
        else:
            flash("Invalid username or password.", "error")

    return render_template("login.html")


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if register_user(username, password):
            flash("Registration successful! You can now log in.", "success")
            return redirect("/login")
        else:
            flash("Username already exists. Try another one.", "error")

    return render_template("register.html")


@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        flash("You need to log in first!", "error")
        return redirect("/login")
    
    user_id = session["user_id"]
    user = get_user_by_id(user_id)
    matrix = EisenhoverMatrix()
    
    current_tasks = matrix.show_current_tasks(user_id)
    
    return render_template("dashboard.html", user=user, current_tasks=current_tasks)



@app.route("/add_task", methods=["POST"])
def add_task():
    if "user_id" not in session:
        flash("You need to log in first!", "error")
        return redirect("/login")
    
    task = request.form["task"]
    task_type = request.form["task_type"]
    quadrat_name = request.form["table_name"]
    user_id = session["user_id"]
    
    matrix = EisenhoverMatrix()
    breakdown_problem = chat_gpt_response(task)
    
    if breakdown_problem:
        try:
            matrix.add_task(quadrat_name, task, breakdown_problem, task_type, user_id)
            flash("Task added successfully!", "success")
        except Exception as e:
            flash(f"Error: {str(e)}", "error")
    
    # 👇 Redirect instead of render_template
    return redirect(url_for("dashboard"))




@app.route("/delete_task", methods=["POST"])
def delete_task():
    if "user_id" not in session:
        flash("You need to log in first!", "error")
        return redirect("/login")

    task = request.form["task"]
    table_name = request.form["table_name"]

    matrix = EisenhoverMatrix()
    try:
        matrix.delete_task(table_name, task)
        flash("Task deleted successfully!", "success")
    except Exception as e:
        flash(f"Error deleting task: {str(e)}", "error")

    return redirect(url_for("dashboard"))



if __name__ == "__main__":
    application.debug = True
    application.run()