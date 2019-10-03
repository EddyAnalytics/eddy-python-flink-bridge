import os

# load config from env variables
BOOTSTRAP_SERVERS = os.environ.get("BOOTSTRAP_SERVER", "kafka:9092")
REDIS_HOST = os.environ.get("REDIS_HOST", "redis:6379")
KAFKA_PLUGIN_VERSION = os.environ.get("KAFKA_PLUGIN_VERSION", "0.9")
