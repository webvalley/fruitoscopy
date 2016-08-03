import os
import tarfile
from utils import time_now

HOME_PATH  = os.path.dirname(os.path.abspath(__file__))

def prepare_download_tar():
    export = tarfile.open(HOME_PATH + '/static/data.tar', mode='w:gz')
    export.add(HOME_PATH + '/static/samples.db',arcname='/samples.db')
    time = time_now()
    export.add(HOME_PATH + '/images', arcname=('/images_'+str(time)))
    export.close()
