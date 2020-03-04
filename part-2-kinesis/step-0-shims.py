#!/usr/bin/env python3

from kafka import KafkaProducer, KafkaConsumer
from kafka.errors import KafkaError

from common import get_prefix, get_brokers

import boto3
import json
import time


# Build up a mapping of Kafka Topic Name => Kinesis Stream Name
prefix = get_prefix()

if prefix is None:
    raise Exception("Unable to find prefix?")

topic_to_stream = {
    "customers": "{prefix}-customer-stream".format(prefix=prefix),
    "orders":    "{prefix}-order-stream".format(prefix=prefix),
    "invoices":  "{prefix}-invoice-stream".format(prefix=prefix),
    "shipments": "{prefix}-shipment-stream".format(prefix=prefix),
}


# Build a list of Kafka Consumers => Kinesis Stream Names
brokers = get_brokers()
consumers = []

for topic_name, stream_name in topic_to_stream.items():
    consumer = KafkaConsumer(
        topic_name,
        bootstrap_servers=brokers,
        value_deserializer=lambda m: json.loads(m.decode("utf-8")),
        auto_offset_reset="earliest",
        enable_auto_commit=True,
    )

    consumer.topics()
    consumer.seek_to_beginning()

    consumers.append((consumer, stream_name))


# Iterate over the Consumers, read all messages, post to Kinesis Stream
kinesis = boto3.client("kinesis")

while True:
    for consumer, stream_name in consumers:
        response = consumer.poll()

        i = 0
        for partition, records in response.items():
            for record in records:
                i += 1

                kinesis.put_record(
                    StreamName=stream_name,
                    Data=json.dumps(record.value).encode("utf-8"),
                    PartitionKey=record.value["id"],
                )

        if i:
            print("Sent {i} messages to {stream}".format(i=i, stream=stream_name))

    time.sleep(2)
