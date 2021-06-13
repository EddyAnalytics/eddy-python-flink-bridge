FROM flink:1.13.1

# install python3 and pip3
RUN apt-get update -y && \
    apt-get install -y python3.7 python3-pip python3.7-dev && rm -rf /var/lib/apt/lists/*

RUN ln -s /usr/bin/python3 /usr/bin/python

COPY requirements.txt .

RUN pip3 install -r requirements.txt --no-cache-dir

COPY . .

COPY sql-client-defaults.yaml /opt/flink/conf/sql-client-defaults.yaml

ENTRYPOINT ["./docker-entrypoint.sh"]
CMD ["eddy-python-flink-bridge"]