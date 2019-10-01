import config
import codecs
import logging
import platform
import sys

from pyflink.common import *
from pyflink.dataset import *
from pyflink.datastream import *
from pyflink.table import *
from pyflink.table.catalog import *
from pyflink.table.descriptors import *
from pyflink.table.window import *


# get arguments from command line
in_topic = str(sys.argv[1])
out_topic = str(sys.argv[2])
sql = str(sys.argv[3])
logging.info("in_topic: {} | out_topic: {} | sql: {}".format(in_topic, out_topic, sql))

# setup the stream execution and stream table environment
s_env = StreamExecutionEnvironment.get_execution_environment()
st_env = StreamTableEnvironment.create(s_env)

# in and output table config
kafka_plugin_version = '0.9'

# input table config
input_table_payload_schema = "ROW<`ts_ms` LONG, `after` ROW<`id` LONG, `first_name` VARCHAR, `last_name` VARCHAR, `email` VARCHAR>, `before` ROW<`id` LONG, `first_name` VARCHAR, `last_name` VARCHAR, `email` VARCHAR>>"
input_table_name = in_topic.split('.')[-1]

st_env \
    .connect(Kafka()
        .version(kafka_plugin_version)
        .topic(in_topic)
        .start_from_earliest()
        .property("bootstrap.servers", config.BOOTSTRAP_SERVERS)) \
    .with_format(
        Json().derive_schema()) \
    .with_schema(
        Schema()
            .field("payload", input_table_payload_schema)) \
    .in_append_mode() \
    .register_table_source(input_table_name)

# output table config
output_table_name = out_topic.split('.')[-1]

st_env \
    .connect(Kafka()
        .version(kafka_plugin_version)
        .topic(output_table_name)
        .property("bootstrap.servers", config.BOOTSTRAP_SERVERS)) \
    .with_format(
        Json().derive_schema()) \
    .with_schema(
        Schema()
            .field("id", DataTypes.BIGINT())
            .field("value", DataTypes.BIGINT())
        ) \
    .in_append_mode() \
    .register_table_sink(output_table_name)


st_env.sql_update(sql)
st_env.execute("celery_sql")

