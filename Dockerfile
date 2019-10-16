FROM eddyanalytics/eddy-flink:latest

WORKDIR /usr/src/app

COPY requirements.txt .

RUN apt-get update \
    && apt-get install -y python3 python3-pip build-essential procps \
    && pip3 install --no-cache-dir -r requirements.txt \
    && apt-get remove -y --purge build-essential \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*

COPY . .

EXPOSE 8000

ENTRYPOINT ["./docker-entrypoint.sh"]
CMD ["eddy-python-flink-bridge"]

