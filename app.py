# -*- coding: utf-8 -*-
import json
import logging
import subprocess
from collections import OrderedDict

from celery import Celery
from kafka import KafkaProducer

import config

app = Celery("app", broker="redis://{}:6379".format(config.REDIS_HOST))

@app.task
def submit_flink_sql(definition):
    logging.info(definition)
    definition = json.loads(definition)

    filename = "./jobs/{}.{}.{}.sql".format(definition["id"], definition["projectId"], definition["pipelineId"]
    file = open(filename, "w")
    file.write(definition["queries"])
    file.close()

    process = subprocess.Popen(
        ["./bin/sql-client.sh", "embedded", "-l", "sql-jars", "-f", filename],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    stdout, stderr = process.communicate()
    stdout, stderr = stdout.decode("utf-8"), stderr.decode("utf-8")

    feedback = {"id": definition["id"], "success": not bool(stderr)}

    logging.info(stdout)
    if stderr:
        feedback["error"] = stderr
        logging.error(stderr)
    else:
        feedback["jobId"] = stdout.strip().split("JobID ")[1]

    producer = KafkaProducer(bootstrap_servers=config.BOOTSTRAP_SERVERS)
    future = producer.send(
        "{}.{}.feedback".format(
            definition["projectId"], definition["pipelineId"]),
        json.dumps(feedback).encode("utf-8"),
    )
    result = future.get(timeout=10)

    return (stdout, stderr)
