import os
from flask import Flask, request, redirect, url_for, flash, render_template
import shutil
import time
import datetime
import sqlite3 as lite
import numpy as np

HOME_PATH  = os.path.dirname(os.path.abspath(__file__))

def insert_in_database(picker,field,timestamp,spectrum,gps):
    """
    This function receive as input the information about what to insert as a new row into the database
    This function has no return.

    The purpose of this function is to insert new data from the samples into the database.

    Specifically:
    @@@@@@@@@@@@@

    :Values in input:
    ----------
    :value 0: The number of the picker
    :value 1: The number of the field
    :value 2: The current timestamp
    :value 3: The list (or the tuple) where the spectrum is saved (as a list/tuple of float)
    :value 4: gps informations (not implemented yet)

    :Return values:
    ----------
    - The HTML page with all the informations about the sample (and te spectrum)
    """
    con= lite.connect(HOME_PATH + "/static/samples.db")
    cur = con.cursor()
    to_execute = ("INSERT INTO Samples (picker,field,timestamp,spectrum,gps) VALUES (%d,%d,%d,\"%s\",\"%s\")" % (picker,field,timestamp,",".join(map(str, spectrum)),gps))
    cur.execute(to_execute)
    con.commit()
    con.close()

def get_from_database(date_from, date_to):
    """
    This function has no input.
    The return is the tuple with all the information on the database.

    The purpose of this function is to list all the samples available on the database.

    Specifically:
    @@@@@@@@@@@@@

    :Return values:
    ----------
    - The tuple with all the information

    Tuple -> (row1,row2, ... ,rown)

    Where rown -> (field1, field2, ... , fieldn)

    """
    con= lite.connect(HOME_PATH + "/static/samples.db")
    cur = con.cursor()

    to_execute = ("SELECT * FROM Samples")
    if(date_from != None and date_to != None):
        to_execute += " WHERE timestamp BETWEEN "
        timestamp = time.mktime(datetime.datetime.strptime(date_from, "%Y-%m-%d").timetuple())
        to_execute += str(int(timestamp))
        to_execute += " AND "
        timestamp = time.mktime(datetime.datetime.strptime(date_to, "%Y-%m-%d").timetuple())
        to_execute += str(int(timestamp))

    cur.execute(to_execute)
    con.commit()
    result = cur.fetchall()
    con.close()
    return result

def get_data_by_id(id_db):
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
    con= lite.connect(HOME_PATH + "/static/samples.db")
    cur = con.cursor()
    to_execute = ("SELECT * FROM Samples WHERE id=" + str(id_db))
    cur.execute(to_execute)
    con.commit()
    result = cur.fetchone()
    con.close()
    spectrum = result[4].split(",")
    print(spectrum[1])
    return spectrum

def delete_data_by_id(id_db):
    """
    This function receive as input the id of the row of the database.
    There is no return value

    The purpose of this function is to delete from the SQLite database a row of the database.

    Specifically:
    @@@@@@@@@@@@@

    :Values in input:
    ----------
    :value 0: The id of the row to delete

    :Return values:
    ----------
    - nothing
    """

    con= lite.connect(HOME_PATH + "/static/samples.db")
    cur = con.cursor()
    to_execute = ("DELETE FROM Samples WHERE id=" + str(id_db))
    cur.execute(to_execute)
    con.commit()
    con.close()

def get_params():
    """
    This function receive as input nothing.
    The return value is a tuple with all the parameters saved into the SQLite DB.

    The purpose of this function is to get all the parameters needed by the image processing algorithm
    so that those can be changed easily thanks to a database query.

    Specifically:
    @@@@@@@@@@@@@

    :Params:
    ----------
    :param 0: Left margin of image to crop
    :param 1: Top margin of image to crop
    :param 2: Left margin of image to crop
    :param 3: Bottom margin of image to crop
    :param 4: Degrees to rotate the image (+ is CCW)
    """

    con= lite.connect(HOME_PATH + "/static/samples.db")
    cur = con.cursor()
    to_execute = ("SELECT * FROM Params")
    cur.execute(to_execute)
    con.commit()
    result = cur.fetchone()
    con.close()
    param = result
    return param

def update_calib_params(params):
    """
    This function receive as input the params to update into the database.
    The return value is a tuple with all the parameters saved into the SQLite DB.

    The purpose of this function is to update the parameters for the image processing.

    Specifically:
    @@@@@@@@@@@@@

    :Params:
    ----------
    :param 0: Left margin of image to crop
    :param 1: Top margin of image to crop
    :param 2: Left margin of image to crop
    :param 3: Bottom margin of image to crop
    :param 4: Degrees to rotate the image (+ is CCW)
    """

    con= lite.connect(HOME_PATH + "/static/samples.db")
    cur = con.cursor()
    to_execute = ("DELETE FROM Params")
    cur.execute(to_execute)
    con.commit()
    result = cur.fetchone()
    to_execute = ("INSERT INTO Params VALUES (%d,%d,%d,%d,%d)" % (params[0],params[1],params[2],params[3],params[4]))
    cur.execute(to_execute)
    con.commit()
    result = cur.fetchone()
    con.close()


def get_spectrum_param():
    """
    This function receive as input nothing.
    The return value is a tuple with all the parameters of the spectrum wavelenghts saved into the SQLite DB.

    The purpose of this function is to get all the parameters needed by the image processing algorithm
    so that those can be changed easily thanks to a database query.

    Specifically:
    @@@@@@@@@@@@@

    :Params:
    ----------
    :param 0: Blue position
    :param 1: Red position
    """

    con= lite.connect(HOME_PATH + "/static/samples.db")
    cur = con.cursor()
    to_execute = ("SELECT * FROM Spectrum")
    cur.execute(to_execute)
    con.commit()
    result = cur.fetchone()
    con.close()
    param = result
    return param

def update_spectrum_params(params):
    """
    This function receive as input the spectrum wavelenghts params to update into the database.
    The return value is a tuple with all the parameters saved into the SQLite DB.

    The purpose of this function is to update the parameters for the image processing.

    Specifically:
    @@@@@@@@@@@@@

    :Params:
    ----------
    :param 0: Blue position
    :param 1: Red position
    """
    print ("%d %d" % (params[0],params[1]))
    con= lite.connect(HOME_PATH + "/static/samples.db")
    cur = con.cursor()
    to_execute = ("DELETE FROM Spectrum")
    cur.execute(to_execute)
    con.commit()
    result = cur.fetchone()
    to_execute = ("INSERT INTO Spectrum VALUES (%d,%d)" % (params[0],params[1]))
    cur.execute(to_execute)
    con.commit()
    result = cur.fetchone()
    con.close()

def reset_database():
    shutil.copy(HOME_PATH + "/databases/default.db", HOME_PATH + "/static/sampeles.db")
