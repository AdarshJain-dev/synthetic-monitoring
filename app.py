from flask import Flask, render_template, request, redirect, url_for, flash
from db import init_db, get_all_endpoints, add_endpoint, delete_endpoint_by_id
import threading
from monitor import monitor_job

app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.route('/')
def index():
    endpoints = get_all_endpoints()
    return render_template('index.html', endpoints=endpoints)

@app.route('/add', methods=['POST'])
def add():
    name = request.form['name']
    url = request.form['url']
    add_endpoint(name, url)
    flash('Endpoint added successfully!')
    return redirect(url_for('index'))

@app.route('/delete/<int:id>')
def delete(id):
    delete_endpoint_by_id(id)
    flash('Endpoint deleted!')
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    threading.Thread(target=monitor_job, daemon=True).start()
    app.run(debug=True, host='0.0.0.0', port=5000)