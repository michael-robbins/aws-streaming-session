#!/usr/bin/env python3

from kafka import KafkaProducer, KafkaConsumer
from kafka.errors import KafkaError

import datetime
import json
import time


def generate_invoice(order):
    invoice = {
        "invoice_id": order["order_id"] + 100000,
        "order_id": order["order_id"],
        "generated_on": datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S%z"),
        "total": sum(i["price"] for i in order["items"]),
    }

    invoice["total_inc_gst"] = invoice["total"] + (invoice["total"] * 0.10)

    return invoice

def listen_for_orders_forever(consumer, producer):
    for order in consumer:
        invoice = generate_invoice(order)
        producer.send("invoices", key=str(invoice["id"]).encode("utf-8"), value=invoice)
        print(invoice)

if __name__ == "__main__":
    brokers = [
        "broker-1:9092",
        "broker-2:9092",
        "broker-3:9092"
    ]

    producer = KafkaProducer(
        bootstrap_servers=brokers,
        value_serializer=lambda m: json.dumps(m).encode("utf-8"),
    )

    consumer = KafkaConsumer(
        "orders",
        bootstrap_servers=brokers,
        value_deserializer=lambda m: json.loads(m.decode("utf-8")),
    )

    listen_for_orders_forever(consumer, producer)
