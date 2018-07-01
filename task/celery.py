from celery import Celery


app = Celery('task', include=['task.tasks'])
app.config_from_object('task.celeryconfig')


if __name__ == '__main__':
    app.start()

# set FORKED_BY_MULTIPROCESSING = 1
# celery -A task worker --loglevel=info
