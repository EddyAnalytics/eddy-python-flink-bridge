import config
import codecs
import logging
import platform
import sys
import json
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
in_schema_info = json.loads(str(sys.argv[4]))
out_schema_info = json.loads(str(sys.argv[5]))
logging.info("in_topic: {} | out_topic: {} | sql: {} | in_schema_info {} | out_schema_info {}".format(in_topic, out_topic, sql, in_schema_info, out_schema_info))

# setup the stream execution and stream table environment
s_env = StreamExecutionEnvironment.get_execution_environment()
st_env = StreamTableEnvironment.create(s_env)

# input table config
input_table_name = in_topic.split('.')[-1]
in_schema = Schema()
for key, value in in_schema_info.items():
    in_schema = in_schema.field(key, value)

st_env \
    .connect(Kafka()
        .version(config.KAFKA_PLUGIN_VERSION)
        .topic(in_topic)
        .start_from_earliest()
        .property("bootstrap.servers", config.BOOTSTRAP_SERVERS)) \
    .with_format(
        Json().derive_schema()) \
    .with_schema(in_schema) \
    .in_append_mode() \
    .register_table_source(input_table_name)

# output table config
output_table_name = out_topic.split('.')[-1]
out_schema = Schema()
for key, value in out_schema_info.items():
    out_schema = out_schema.field(key, value)

st_env \
    .connect(Kafka()
        .version(kafka_plugin_version)
        .topic(out_topic)
        .property("bootstrap.servers", config.BOOTSTRAP_SERVERS)) \
    .with_format(
        Json().derive_schema()) \
    .in_append_mode() \
    .with_schema(out_schema) \
    .register_table_sink(output_table_name)

# run the sql statement
st_env.sql_update(sql)
st_env.execute("celery_sql")

