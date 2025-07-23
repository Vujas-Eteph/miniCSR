# run with: gunicorn -w 4 -b 0.0.0.0:1990 app:app

from flask import Flask, render_template, request, redirect, url_for, session, flash
import json  # Import json to read the JSON file

app = Flask(__name__)
app.secret_key = 'my super secret key'.encode('utf8')

# Password to log to you website
PASSWORD = "0000"  # ! Adapt this !

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        password = request.form['password']
        if password == PASSWORD:
            session['authenticated'] = True
            return redirect(url_for('display_output'))
        else:
            flash("Incorrect password, please try again.")
    return render_template('login.html')  # Ensure 'login.html' exists in your templates folder

@app.route('/CSR')
def display_output():
    if not session.get('authenticated'):
        return redirect(url_for('login'))

    # Decode JSON file
    try:
        with open("data.json", "r") as file:
            loaded_data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        flash("Error loading data: " + str(e))
        return redirect(url_for('logout'))

    # Render the data in 'main.html'
    return render_template('main.html',
                           result=loaded_data.get("stats", "No stats available"),
                           result_detailed_gpu=loaded_data.get("detailed_stats_gpu", "No detailed stats available"),
                           result_detailed_cpu=loaded_data.get("detailed_stats_cpu", "No detailed stats available"),
                           result_detailed_space=loaded_data.get("disk_stats", "No disk stats available"))

@app.route('/logout')
def logout():
    session.pop('authenticated', None)
    return redirect(url_for('login'))

@app.route('/shutdown', methods=['GET'])
def shutdown():
    if not session.get('authenticated'):
        return redirect(url_for('login'))
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        return "Could not find the Werkzeug server shutdown function."
    func()
    return 'Server shutting down...'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1990)
