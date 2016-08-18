import os
from flask import Flask, request, redirect, url_for, flash, render_template
from werkzeug.utils import secure_filename
import time
import sqlite3 as lite
import scipy.signal as sps
#from matplotlib.pylab import savefig
from PIL import Image
import datetime
from signal_processing import *
from database_interactions import *
from export_db import prepare_download_tar
import base64
import json
from shutil import copyfile
from utils import *
from apply_config import *
import random

HOME_PATH  = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = HOME_PATH + '/temp_data'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/data_taken', methods=['GET', 'POST'])
def data_taken():
    """
    Process the request from the data_take page
    Returns OK if the process has been executed correctly

    TODO: return also machine learning prediction
    """

    fruit = int(request.form.get('fruit'))
    gps = request.form.get('gps')
    if gps == None:
        gps = ""
    tmstp = time_now()
    processed = process_image()
    if(processed[0] == -1):
        return "CALIBRATION DONE"
    spectrum = processed[1].tolist()
    if processed[0] == 1:
        result = "READY TO BE HARVESTED"
    elif processed[0] == 0:
        result = "NOT GOOD"
    else:
        result = "TOO GOOD TO BE EATEN"


    insert_in_database(fruit=fruit, spectrum=spectrum, gps=gps, tmstp=tmstp, label=processed[0])
    return ("OK,," + str(get_last_id_inserted()) +',,' + processed[2] +',,' + processed[3] + ",," + result)
    #return ("OK,," + str(get_last_id_inserted()))
    #return render_template('data_taken.html', field=field, result=result)

@app.route('/take_data', defaults={'fruit': 1})
@app.route('/take_data/<int:fruit>')
def take_data(fruit):
    """
    This function receive as input (POST request) the number of the field where the picker is working.
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
    if(not os.path.isfile(HOME_PATH + '/static/processed_white.png')):
        get_white = 1
    else:
        get_white = 0

    return render_template('take_data.html', fruit=fruit, get_white=get_white)


@app.route('/sync_timestamp', methods=['GET', 'POST'])
def sync_timestamp():
    """
    This function receive as input (POST request) the current phone timestamp.
    The return is the confirmation that the sync happened.

    The purpose of this function is to sync the raspberry, because has no battery inside.

    Specifically:
    @@@@@@@@@@@@@

    :Return values:
    ----------
    - OK if the sync is made, nothing if something bad happens
    """
    try:
        timestamp = request.form['timestamp']
    except:
        print("Unable to retrieve timestamp from post request")
    try:
        update_time(timestamp)
    except:
        print("Unable to update_time")
    return "OK"

@app.route('/')
def show_html():
    """
    Open the index page
    """
    return render_template('index.html')

@app.route('/get_db')
def download_db():
    """
    show the page to download the database from the raspberry into the device
    """
    prepare_download_tar()
    return render_template('get_db.html')

@app.route('/send_file')
def upload_conf_file():
    """
    Show the page to send a new configuration file
    """
    return render_template('send_file.html')

@app.route('/send_file_done', methods=['GET', 'POST'])
def upload_conf_file_done():
    """
    Show the page to send the database to the server (the django one that will be deployed)
    """
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return 'No file part'
        file = request.files.get('file')
        # if user does not select file, browser also
        # submit a empty part without filename
        if file == None:
            return "No selected file"


        if file and ("config" in file.filename and ".tar" in file.filename):
            #filename = secure_filename(file.filename)
            filename = file.filename
            file.save(os.path.join(HOME_PATH + "/temp_data", filename))
            result = apply_configuration(filename = filename)
            if result == 1:
                return render_template('send_file_done.html')
            else:
                return "Error"
    return "Error"

@app.errorhandler(404)
def page_not_found(error):
    """
    If a non-handled error happens, show the 404 error page
    """
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(error):
    """
    If a non-handled error happens, show the 500 error page
    """
    return render_template('500.html'), 500

@app.route('/database_info', defaults={'date_from': None, 'date_to': None})
@app.route('/database_info/<date_from>/<date_to>')
def show_database_info(date_from,date_to):
    """
    This function receive as input nothing.
    The return is the page that shows all the records of the samples in the database of the raspberry.

    The purpose of this function is to show a summary of the informations into the database and give the user
    the possibility to access more informations.

    Specifically:
    @@@@@@@@@@@@@

    :Return values:
    ----------
    - The database HTML page
    """
    rows_a = get_from_database(date_from, date_to)
    rows = list(list(i) for i in rows_a)

    for i in range(len(rows)):
        rows[i][5] = datetime.datetime.fromtimestamp(rows[i][5]).strftime('%d-%m-%Y %H:%M:%S')
    if(date_from != None and date_to != None):
        return render_template('show_database.html',rows=rows,date_from=date_from, date_to=date_to)
    else:
        return render_template('show_database.html',rows=rows,date_from="2016-01-01", date_to=datetime.datetime.fromtimestamp(time_now()).strftime('%Y-%m-%d'))


@app.route('/more_info', methods=['GET', 'POST'])
def show_more_info():
    """
    This function receive as input the id of the database.
    The return is the page with the informations about the data of the sample that has been requested.

    The purpose of this function is to show more informations about a specific sample that has been taken by the device and that
    is still in the database.

    Specifically:
    @@@@@@@@@@@@@

    :Values in input:
    ----------
    :value 0: The id of the sample to show

    :Return values:
    ----------
    - The HTML page with all the informations about the sample (and te spectrum)
    """
    id_db = p_0 = int(request.form['id'])
    data = get_data_by_id(id_db)
    spectrum =  data[1].split(",")
    spectrum = [float(x) for x in spectrum]
    script, div = save_plot(spectrum, range(400,801),controls=1)
    photo = 0
    if(data[8] != None):
        copyfile(HOME_PATH + '/images/' +str(data[8]), HOME_PATH + '/static/photo_associated.jpg')
        photo = 1
    return ("OK,,%d,,%d,,%s,,%d,,%d,,%d,,%d,,%s,,%s" % (data[2],data[3],data[4],data[5],data[6],data[7],photo,script,div))
    #return render_template('more_info_from_row.html', id_db=id_db)

@app.route('/delete_data/<int:id_db>')
def delete_data(id_db):
    """
    This function is just the route to the delete_data function.
    The documentation about the deletion of the data can be found there.
    """
    delete_data_by_id(id_db)
    return render_template('row_deleted.html')

@app.route('/calib_crop_rotate', methods=['GET', 'POST'])
def calib_crop_rotate():
    """
    Returns the index page for area calibration
    """
    return render_template('calib_crop_rotate.html',param=get_params())

@app.route('/calib_crop_rotate_done', methods=['GET', 'POST'])
def calib_crop_rotate_done():
    """
    Gets the data from the area calibration page and upload them into the database
    """

    p_0 = int(request.form['param_0'])
    p_1 = int(request.form['param_1'])
    p_2 = int(request.form['param_2'])
    p_3 = int(request.form['param_3'])
    p_4 = int(request.form['param_4'])

    param = (p_0,p_1,p_2,p_3,p_4)
    update_calib_params(param)
    get_image()
    return "OK"
    return render_template('calib_crop_rotate_done.html')

@app.route('/calib_spectrum')
def calib_spectrum():
    return render_template('calib_spectrum.html', param=get_spectrum_param(), dim =get_params())

@app.route('/calib_spectrum_done', methods=['GET', 'POST'])
def calib_spectrum_done():
    blue = int(request.form.get('blue'))
    red = int(request.form.get('red'))
    if(blue == None or red == None):
        return "ERROR"
    update_spectrum_params((blue,red))
    return "OK"
    #return render_template('calib_spectrum_done.html', param=get_spectrum_param())

@app.route('/reset_database', methods=['GET', 'POST'])
def reset_database_route():
    reset = request.form.get('reset')
    if(reset == 'entire_database'):
        reset_all_database()
    elif(reset == 'only_samples'):
        reset_samples()
    return "OK"
    #return render_template('calib_spectrum_done.html', param=get_spectrum_param())

@app.route('/update_label', methods=['GET', 'POST'])
def update_label():
    id = request.form.get('id')
    label = request.form.get('label')
    label_update_db(id,label)
    return "OK"

@app.route('/upload_img', methods=['GET', 'POST'])
def upload_img():
    received = request.get_json()
    img = received['imageData']
    id = received['id_db']
    #id = id[1:]
    g = open("out.png", "wb")
    g.write(base64.b64decode(img))
    g.close()
    im = Image.open('out.png')
    im.save('out.jpg')
    insert_image(id)
    msg = 'Image uploaded'
    status = "success"
    return json.dumps({"status" : status, "msg" : msg})

@app.route('/get_just_image', methods=['GET', 'POST'])
def get_just_image():
    get = request.form.get('get')
    if(get == 'yes'):
        get_image(new_photo=1)
        return "OK"
    else:
        return "Error, post request was not made correctly"

@app.route('/calibrate_white')
def calibrate_white():
    return render_template('calib_white.html')

@app.route('/calibrate_white_done', methods=['GET', 'POST'])
def calibrate_white_done():
    processed = get_image(white_calibration = 1)
    return "OK"

if __name__ == "__main__":
    """
    Just start the server open to everyone, on the port 5000
    """
    if(not os.path.isfile(HOME_PATH + '/static/samples.db')):
        create_database_first_time()
    if(not os.path.isfile(HOME_PATH + '/source.jpg')):
        print("Getting first source")
        get_image(new_photo=1)
    if(not os.path.isdir(HOME_PATH + '/images')):
        os.system("mkdir " + HOME_PATH + '/images')
    if(not os.path.isdir(HOME_PATH + '/configuration')):
        os.system("mkdir " + HOME_PATH + '/configuration')
    if(not os.path.isdir(HOME_PATH + '/temp_data')):
        os.system("mkdir " + HOME_PATH + '/temp_data')
    if(os.path.isfile(HOME_PATH + '/static/processed_white.png')):
        os.system("rm " + HOME_PATH + '/static/processed_white.png')
    if(not os.path.isfile(HOME_PATH + '/timestamp.txt')):
        out_file = open(HOME_PATH + '/timestamp.txt',"w")
        out_file.write(str(0))
        out_file.close()
    app.run(host='0.0.0.0')
