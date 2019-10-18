from celery import Celery
from kafka import KafkaProducer
from collections import OrderedDict
import subprocess
import config
import logging
import json

app = Celery('app', broker="redis://{}:6379".format(config.REDIS_HOST))

@app.task
def submit_flink_sql(definition):
    logging.info(definition)
    process = subprocess.Popen(['./docker-entrypoint.sh', 'python3', 'sql.py', definition], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    stdout, stderr = stdout.decode('utf-8'), stderr.decode('utf-8')

    definition = json.loads(definition)
    feedback = {
	"id": definition["id"],
        "success": not bool(stderr)
    }

    logging.info(stdout)
    if stderr:
        feedback["error"] = stderr
        logging.error(stderr)
    else:
        feedback["jobId"] = stdout.strip().split("JobID ")[1]

    producer = KafkaProducer(bootstrap_servers=config.BOOTSTRAP_SERVERS)
    future = producer.send("{}.{}.feedback".format(definition["projectId"], definition["pipelineId"]), json.dumps(feedback).encode('utf-8'))
    result = future.get(timeout=10)

    return (stdout, stderr)

