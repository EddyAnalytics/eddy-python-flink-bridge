# -*- coding: utf-8 -*-
import os

# load config from env variables
BOOTSTRAP_SERVERS = os.environ.get("BOOTSTRAP_SERVER", "kafka:9092")
REDIS_HOST = os.environ.get("REDIS_HOST", "redis:6379")
FLINK_HOST = os.environ.get("FLINK_HOST", "flink-jobmanager")
FLINK_PORT = os.environ.get("FLINK_PORT", "8081")


