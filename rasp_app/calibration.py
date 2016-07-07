import os
from flask import Flask, request, redirect, url_for, flash, render_template
from werkzeug.utils import secure_filename
import time
import sqlite3 as lite
import numpy as np

HOME_PATH  = os.path.dirname(os.path.abspath(__file__))


def get_white_spectrum():
    white_spectrum = np.genfromtxt(HOME_PATH + '/white_cal.txt', delimiter=' ')
    return white_spectrum
