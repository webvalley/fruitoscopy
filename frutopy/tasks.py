from celery import Celery
import tempfile
import tarfile
import shutil
from frutopy.local_settings import BASE_IMG_DIR, INPUT_DB
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
        tfile.extractall(destination)
        dir_name = get_dir(destination)[0]
        print(dir_name)
        shutil.move(get_dir(destination)[1], BASE_IMG_DIR)
        write_central_db(read_db(os.path.join(destination, INPUT_DB)), dir_name)
        print("Done you motherfucker")


