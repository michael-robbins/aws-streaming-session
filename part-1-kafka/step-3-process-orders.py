#!/usr/bin/env python3

from kafka import KafkaProducer, KafkaConsumer
from kafka.errors import KafkaError
from common import get_brokers

import datetime
import json
import time
import uuid


def generate_invoice(order):
    invoice = {
        "invoice_id": str(uuid.uuid4()),
        "order_id": order["order_id"],
        "customer_id": order["customer_id"],
        "generated_on": datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S%z"),
        "total": sum(i["price"] for i in order["items"]),
    }

    invoice["total_inc_gst"] = round(invoice["total"] + (invoice["total"] * 0.10), 2)

    return invoice


if __name__ == "__main__":
    brokers = get_brokers()

    producer = KafkaProducer(
        bootstrap_servers=brokers,
        value_serializer=lambda m: json.dumps(m).encode("utf-8"),
    )

    orders_consumer = KafkaConsumer(
        "orders",
        bootstrap_servers=brokers,
        value_deserializer=lambda m: json.loads(m.decode("utf-8")),
        auto_offset_reset="earliest",
        enable_auto_commit=True,
    )

    while True:
        response = orders_consumer.poll()

        for partition, orders in response.items():
            for order in orders:
                invoice = generate_invoice(order.value)
                producer.send("invoices", invoice)
                print(invoice)

        time.sleep(1)
