from celery import Celery
import tempfile
import tarfile
import shutil
from frutopy.local_settings import BASE_IMG_DIR
from utils import *

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
        print("Reading SQLITE database and wirting to PostgreSQL")
        write_central_db(read_db("samples.db"))
        print("Done you motherfucker")
        print(get_dir(destination))
        shutil.move(get_dir(destination), BASE_IMG_DIR)
    print("Unzipped at: %s" % destination)


