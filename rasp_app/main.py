import os
from flask import Flask, request, redirect, url_for, flash, render_template
from werkzeug.utils import secure_filename
import time
import sqlite3 as lite
from signal_processing import *
import scipy.signal as sps
from matplotlib.pylab import savefig
from PIL import Image
import datetime

UPLOAD_FOLDER = ''
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif','db'])
HOME_PATH  = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__, instance_path='/path/to/instance/folder')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def time_now():
    in_file = open(HOME_PATH + "/timestamp.txt","r")
    text = in_file.read()
    from_file = int(text)
    time_to_send = int(time.time()) + from_file
    return time_to_send

def update_time(timestamp):
    out_file = open(HOME_PATH + "/timestamp.txt","w")
    diff_time = int(float(timestamp))-int(time.time())
    out_file.write(str(diff_time))
    out_file.close()
    
def insert_in_database(picker,field,timestamp,spectrum,gps):
    con= lite.connect(HOME_PATH + "/static/samples.db")
    cur = con.cursor()
    to_execute = ("INSERT INTO Samples (picker,field,timestamp,spectrum,gps) VALUES (%d,%d,%d,\"%s\",\"%s\")" % (picker,field,timestamp,",".join(map(str, spectrum)),gps))
    cur.execute(to_execute)
    con.commit()
    con.close()
    
def get_from_database():
    
    con= lite.connect(HOME_PATH + "/static/samples.db")
    cur = con.cursor()
    
    to_execute = ("SELECT * FROM Samples")
    cur.execute(to_execute)
    con.commit()
    result = cur.fetchall()
    con.close()
    return result

def get_data_by_id(id_db):
    con= lite.connect(HOME_PATH + "/static/samples.db")
    cur = con.cursor()
    to_execute = ("SELECT * FROM Samples WHERE id=" + str(id_db))
    cur.execute(to_execute)
    con.commit()
    result = cur.fetchone()
    con.close()
    spectrum = result[4].split(",")
    print(spectrum)
    return spectrum

def delete_data_by_id(id_db):
    """
    This function receive as input the id of the database.
    The return is the page that confirm the row of the id has been deleted from the database.
    
    The purpose of this function is to delete from the SQLite database a row of the database.
    
    Specifically:
    @@@@@@@@@@@@@
    
    :Values in input:
    ----------
    :value 0: The id of the row to delete
    
    :Return values:
    ----------
    - The confirmation HTML page
    """
    
    con= lite.connect(HOME_PATH + "/static/samples.db")
    cur = con.cursor()
    to_execute = ("DELETE FROM Samples WHERE id=" + str(id_db))
    cur.execute(to_execute)
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
                file.save(os.path.join(HOME_PATH + "/databases", filename))
                return 'Everything worked, but your file will be deleted because the system is not ready yet'
        except:
            return "unable to work with full file"
    return "Not a POST request"

@app.route('/data_taken', methods=['GET', 'POST'])
def data_taken():
    field = int(request.form['field'])
    #result = "NOT RIPE YET"
    #time.sleep(0)
    picker = 1
    gps = "n/d"
    timestamp = time_now()
    
    #try:
    processed = process_image()
    spectrum = processed[1].tolist()
    #    try:
    insert_in_database(picker, field, timestamp, spectrum,gps)
    #    except:
    #        print("Unable to insert into database")
    #except:
    #    print("Unable to process image")
    if processed[0]:
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
    print(HOME_PATH)
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

@app.route('/database_info')
def show_database_info():
    try:
        rows_a = get_from_database()
    except:
        print("Unable to get data from database")
        return render_template('500.html'), 500
    rows = list(list(i) for i in rows_a)

    for i in range(len(rows)):
        rows[i][3] = datetime.datetime.fromtimestamp(rows[i][3]).strftime('%d-%m-%Y %H:%M:%S')
    
    return render_template('show_database.html',rows=rows)


@app.route('/more_info/<int:id_db>')
def show_more_info(id_db):
    try:
        spectrum = get_data_by_id(id_db)
    except:
        print("Unable to get spectrum from database")
        return render_template('500.html'), 500
    
    #try:
    spectrum = [float(x) for x in spectrum]
    save_plot(spectrum)
    #except:
        #print("Unable to save plot")
    
    return render_template('more_info_from_row.html', id_db=id_db)

@app.route('/delete_data/<int:id_db>')
def delete_data(id_db):
    
    
    delete_data_by_id(id_db)
    
    return render_template('row_deleted.html')
    
        
    
    
if __name__ == "__main__":
    """
    Just start the server open to everyone, on the port 5000
    """
    app.run(host='0.0.0.0')