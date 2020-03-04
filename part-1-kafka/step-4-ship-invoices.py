#!/usr/bin/env python3

from kafka import KafkaProducer, KafkaConsumer
from kafka.errors import KafkaError
from common import get_brokers

import datetime
import json
import time
import uuid


CUSTOMERS = {}


def generate_shipment(invoice):
    shipment = {
        "shipment_id": str(uuid.uuid4()),
        "invoice_id": invoice["invoice_id"],
        "order_id": invoice["order_id"],
        "customer_id": invoice["customer_id"],
        "generated_on": datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S%z"),
        "destination": CUSTOMERS[invoice["customer_id"]]["location"],
    }

    return shipment


def update_customers(consumer):
    response = customer_consumer.poll()

    i = 0
    for partition, customers in response.items():
        for customer in customers:
            i += 1

            CUSTOMERS[customer.value["id"]] = customer.value

    if i:
        print("Updated {0} customers".format(i))


if __name__ == "__main__":
    brokers = get_brokers()

    producer = KafkaProducer(
        bootstrap_servers=brokers,
        value_serializer=lambda m: json.dumps(m).encode("utf-8"),
    )

    customer_consumer = KafkaConsumer(
        "customers",
        bootstrap_servers=brokers,
        value_deserializer=lambda m: json.loads(m.decode("utf-8")),
        auto_offset_reset="earliest",
        enable_auto_commit=True,
    )

    invoice_consumer = KafkaConsumer(
        "invoices",
        bootstrap_servers=brokers,
        value_deserializer=lambda m: json.loads(m.decode("utf-8")),
        auto_offset_reset="earliest",
        enable_auto_commit=True,
    )

    # Resync the entire customer topic into memory
    customer_consumer.topics()
    customer_consumer.seek_to_beginning()

    while not CUSTOMERS:
        update_customers(customer_consumer)
        time.sleep(0.5)

    # Process invoices forever
    for invoice in invoice_consumer:
        # Update Customers each time
        update_customers(customer_consumer)

        # Process invoices
        shipment = generate_shipment(invoice.value)

        producer.send("shipments", shipment)
        print(shipment)
