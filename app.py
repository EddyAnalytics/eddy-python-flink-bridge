from celery import Celery
import subprocess
import config
import logging

app = Celery('app', broker="redis://{}:6379".format(config.REDIS_HOST))

@app.task
def submit_flink_sql(*args):
    logging.info(args)
    process = subprocess.Popen(['./docker-entrypoint.sh', 'python3', 'sql.py',*args], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    logging.info(stdout)
    if stderr:
        logging.error(stderr)
    return (stdout, stderr)

