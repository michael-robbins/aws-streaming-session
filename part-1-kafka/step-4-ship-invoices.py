#!/usr/bin/env python3

from kafka import KafkaProducer, KafkaConsumer
from kafka.errors import KafkaError

import datetime
import json
import time


def generate_invoice(order):
    shipment = {
        "shipment_id": order["invoice_id"] + 100000,
        "invoice_id": order["invoice_id_id"],
        "order_id": order["order_id"],
        "generated_on": datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S%z"),
    }

    return shipment

def listen_for_orders_forever(consumer, producer):
    for invoice in consumer:
        shipment = generate_shipment(invoice)

        producer.send("shipments", key=str(invoice["id"]).encode("utf-8"), value=shipment)
        print(shipment)

if __name__ == "__main__":
    brokers = [
        "broker-1:9092",
        "broker-2:9092",
        "broker-3:9092",
    ]

    producer = KafkaProducer(
        bootstrap_servers=brokers,
        value_serializer=lambda m: json.dumps(m).encode('utf-8'),
    )

    consumer = KafkaConsumer(
        "invoices",
        bootstrap_servers=brokers,
        value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    )

    listen_for_orders_forever(consumer, producer)
