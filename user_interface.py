from flask import Flask, render_template, request, redirect, flash, url_for

app = Flask(__name__)
app.secret_key = '4b7c3a2b8c9e1d4f7e6a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3d4e5f6a7b8c9d0e'


@app.route('/')
def home():
    return redirect('/login')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password  = request.form['password']

        if not username or not password:
            flash('username and password are required', 'error')
            redirect(url_for('login'))
    return render_template('/login.html')


if __name__ == '__main__':
    app.run(debug=True)