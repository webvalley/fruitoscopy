from celery import Celery

app = Celery('celery_tasks', backend='amqp', broker='amqp://')

@app.task(ignore_result=True)
def process_file(filepath):
    print(filepath)
    # script che legge il file sqlite e butta tutto in postgres