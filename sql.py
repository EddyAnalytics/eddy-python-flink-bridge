import config
import codecs
import logging
import platform
import sys
import json
from collections import OrderedDict
from pyflink.common import *
from pyflink.dataset import *
from pyflink.datastream import *
from pyflink.table import *
from pyflink.table.catalog import *
from pyflink.table.descriptors import *
from pyflink.table.window import *


# get sql job definition from command line
definition = json.loads(str(sys.argv[1]), object_pairs_hook=OrderedDict)
logging.info("sql job definition: {}".format(definition))


# setup the stream execution and stream table environment
s_env = StreamExecutionEnvironment.get_execution_environment()
st_env = StreamTableEnvironment.create(s_env)
s_env.set_stream_time_characteristic(TimeCharacteristic.EventTime)
s_env.set_parallelism(definition.get("parallelism", 1))


def get_kafka_table(topic, table_definition):
    schema = Schema()

    if table_definition["type"] == "source":
        rowtime = Rowtime().timestamps_from_source().watermarks_periodic_bounded(1000)
        schema = schema.field("ts", "SQL_TIMESTAMP").rowtime(rowtime)

    for key, value in table_definition["schema"].items():
        schema = schema.field(key, value)

    return st_env \
        .connect(Kafka()
        .version("universal")
        .topic(topic)
        .start_from_earliest()
        .property("bootstrap.servers", config.BOOTSTRAP_SERVERS)) \
        .with_format(
        Json().derive_schema()) \
    .with_schema(schema) \
    .in_append_mode()


for topic, table_definition in definition["schemas"].items():
    table_name = topic.split('.')[-1]
    table = get_kafka_table(topic, table_definition)
    if table_definition["type"] == "source":
        table.register_table_source(table_name)
    else:
        table.register_table_sink(table_name)

#changes = st_env.sql_query("SELECT ts, payload.after.order_number, payload.after.product_id, payload.before.quantity, payload.after.quantity, (payload.after.quantity - payload.before.quantity) FROM orders WHERE payload.before.quantity <> payload.after.quantity")
#st_env.sql_update("INSERT INTO sql_results SELECT * FROM " + str(changes))
#st_env.sql_update("INSERT INTO sql_results_count SELECT COUNT(*) FROM " + str(changes) + " GROUP BY TUMBLE(ts, INTERVAL '5' SECOND)")

# run the sql statement
for query in definition["queries"]:
    st_env.sql_update(query)
st_env.execute("celery_sql")

