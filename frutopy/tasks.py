from celery import Celery
import tempfile
import tarfile
from utils import *
import os

app = Celery('tasks', backend='amqp', broker='amqp://')

@app.task(ignore_result=True)
def process_file(file_path):
    """
    Untar file and process SQLite database to update main PostgreSQL database
    """
    print("File path: %s" % file_path)
    tfile = tarfile.open(file_path, 'r:gz')
    with tempfile.TemporaryDirectory() as destination:
        print("created temporary directory %s" % destination)
        tfile.extractall(destination)
        db_name = os.path.join(destination, "samples.db")
        write_central_db(read_db(db_name))
    print("Unzipped at: %s" % destination)


