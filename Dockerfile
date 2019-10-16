FROM flink:1.9

WORKDIR /usr/src/app

COPY requirements.txt .

RUN apt-get update \
    && apt-get install -y python3 python3-pip build-essential procps \
    && pip3 install --no-cache-dir -r requirements.txt \
    && apt-get remove -y --purge build-essential \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*

RUN wget http://central.maven.org/maven2/org/apache/flink/flink-json/1.9.0/flink-json-1.9.0-sql-jar.jar -P /opt/flink/lib \
    && wget http://central.maven.org/maven2/org/apache/flink/flink-sql-connector-kafka-0.9_2.11/1.9.0/flink-sql-connector-kafka-0.9_2.11-1.9.0.jar -P /opt/flink/lib

COPY . .

EXPOSE 8000

ENTRYPOINT ["./docker-entrypoint.sh"]
CMD ["eddy-python-flink-bridge"]

