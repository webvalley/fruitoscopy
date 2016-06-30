import os
from flask import Flask, request, redirect, url_for, flash, render_template
from werkzeug.utils import secure_filename
import time
import sqlite3 as lite
from signal_processing import *

UPLOAD_FOLDER = ''
APPLICATION_ROOT = '/home/pi/signal_processing/flask/little_server/'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif','db'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['APPLICATION_ROOT'] =  APPLICATION_ROOT

def time_now():
    in_file = open(home_path + "timestamp.txt","r")
    text = in_file.read()
    from_file = int(text)
    time_to_send = int(time.time()) + from_file
    return time_to_send

def update_time(timestamp):
    out_file = open(home_path + "timestamp.txt","w")
    diff_time = int(float(timestamp))-int(time.time())
    out_file.write(str(diff_time))
    out_file.close()
    
def insert_in_database(picker,field,timestamp,spectrum,gps):
    con = sqlite.connect(home_path + "static/samples.db")
    cur = con.cursor()
    cur.execute("INSERT INTO Samples (picker,field,timestamp,spectrum,gps) VALUES (%d,%d,%d,\"%s\",\"%s\")" % (picker,field,int(time.time()),db_string,gps))
    con.commit()
    con.close()
    
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/db_uploaded', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return 'No file part'
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        try:
            if len(file.filename)<2:
                try:
                    flash('No selected file')
                    return "No selected file"
                except:
                    return "Unable to flash"
        except:
            return "Unable to work with empty file"
        
        try:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(home_path + "/databases", filename))
                return 'Everything worked, but your file will be deleted because the system is not ready yet'
        except:
            return "unable to work with full file"
    return "Not a POST request"

@app.route('/data_taken', methods=['GET', 'POST'])
def data_taken():
    field = request.form['field']
    #result = "NOT RIPE YET"
    #time.sleep(0)
    try:
        processed = process_image()
    except:
        print("Unable to process image")
    if processed:
        result = "IS RIPE"
    else:
        result = "NOT RIPE YET"
    return render_template('data_taken.html', field=field, result=result)

@app.route('/take_data/<int:field>')
def take_data(field):
    return render_template('take_data.html', field=field)

@app.route('/sync_timestamp', methods=['GET', 'POST'])
def sync_timestamp():
    try:
        timestamp = request.form['timestamp']
    except:
        print("Unable to retrieve timestamp from post request")
    try:
        #lolol(1)
        update_time(timestamp)
    except:
        print("Unable to update_time")
    return "OK"

@app.route('/')
def show_html():
    return render_template('index.html')

@app.route('/get_db')
def download_db():
    return render_template('get_db.html')

@app.route('/send_db')
def upload_db():
    return render_template('send_db.html')

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(error):
    return render_template('500.html'), 500

if __name__ == "__main__":
    home_path = "/home/pi/signal_processing/flask/little_server/"
    app.run(host='0.0.0.0')