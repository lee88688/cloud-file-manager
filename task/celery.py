from celery import Celery


app = Celery('task', include=['task.download'])
app.config_from_object('task.celeryconfig')


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kargs):
    sender.add_periodic_task(10.0, 'task.download.refresh')


if __name__ == '__main__':
    app.start()

# set FORKED_BY_MULTIPROCESSING = 1 or powershell: $env:FORKED_BY_MULTIPROCESSING = 1
# celery -A task worker --loglevel=info
