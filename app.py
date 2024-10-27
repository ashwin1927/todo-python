from flask import Flask, render_template, request, redirect, url_for, flash, session
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ashwinisaacaditya'

TASK_FILE = 'tasks.txt'
USERNAME = 'admin'
PASSWORD = 'password'

def read_tasks():
    if not os.path.exists(TASK_FILE):
        return []
    with open(TASK_FILE, 'r') as file:
        return [
            {
                'title': parts[0],
                'description': parts[1],
                'complete': parts[2] == '1'
            }
            for line in file
            for parts in [line.strip().split('|')]
            if len(parts) == 3
        ]

def write_tasks(tasks):
    with open(TASK_FILE, 'w') as file:
        for task in tasks:
            file.write(f"{task['title']}|{task['description']}|{'1' if task['complete'] else '0'}\n")

@app.route('/')
def home():
    return redirect(url_for('index')) if 'logged_in' in session else render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form.get('username') == USERNAME and request.form.get('password') == PASSWORD:
            session['logged_in'] = True
            flash('Logged in Successfully', 'success')
            return redirect(url_for('index'))
        flash('Invalid username or password', 'error')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in')
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))

@app.route('/dashboard')
def index():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    return render_template('index.html', tasks=read_tasks())

@app.route('/add', methods=['POST'])
def add_task():
    if 'logged_in' in session and request.form.get('title'):
        tasks = read_tasks()
        tasks.append({'title': request.form.get('title'), 'description': request.form.get('description', ''), 'complete': False})
        write_tasks(tasks)
        flash('Task added successfully!', 'success')
    return redirect(url_for('index'))

@app.route('/update/<int:task_id>')
def update_task(task_id):
    if 'logged_in' in session:
        tasks = read_tasks()
        if task_id >= 0 and task_id < len(tasks):
            tasks[task_id]['complete'] = not tasks[task_id]['complete']
            write_tasks(tasks)
    return redirect(url_for('index'))


@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    if 'logged_in' in session:
        tasks = read_tasks()
        if 0 <= task_id < len(tasks):
            del tasks[task_id]
            write_tasks(tasks)
            flash('Task deleted!', 'error')
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
