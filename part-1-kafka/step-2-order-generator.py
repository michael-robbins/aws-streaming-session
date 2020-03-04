#!/usr/bin/env python3

from kafka import KafkaProducer, KafkaConsumer
from kafka.errors import KafkaError
from common import get_brokers

import datetime
import random
import json
import time
import uuid


PRODUCTS = [
    {"type": "car", "brand": "Ford", "product": "Falcon XR6", "price": 25000},
    {"type": "car", "brand": "Ford", "product": "Falcon XR8", "price": 28000},
    {"type": "car", "brand": "Holden", "product": "Commodore Tourer", "price": 32000},
    {"type": "food", "brand": "Safeway", "product": "Celery", "price": 0.25},
    {"type": "food", "brand": "Safeway", "product": "Apples", "price": 0.35},
    {"type": "food", "brand": "Heinz", "product": "Tomato Sauce", "price": 2.99},
    {"type": "food", "brand": "Melbourne Hotsauce Company", "product": "Bum Burner", "price": 12.99},
    {"type": "tv", "brand": "Panasonic", "product": "65 4K HDR OLED TV", "price": 2499.99},
    {"type": "tv", "brand": "Samsung", "product": "98 QLED 8K UHD TV", "price": 2099.99},
    {"type": "tv", "brand": "LG", "product": "65 OLED TV", "price": 3599.00},
    {"type": "spirits", "brand": "Laphroaig", "product": "10YO Single Malt Whisky", "price": 89.99},
    {"type": "spirits", "brand": "Ardbeg", "product": "Uigeadail", "price": 120.50},
    {"type": "spirits", "brand": "Bruichladdich", "product": "Sherry Cask Edition 25YO", "price": 850},
]


CUSTOMERS = {}


def generate_items(choices=3):
    return [random.choice(PRODUCTS) for _ in range(random.randrange(1, choices + 1))]


def generate_order():
    return {
        "id": str(uuid.uuid4()),
        "customer_id": random.choice(list(CUSTOMERS.keys())),
        "order_time": datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S%z"),
        "items": generate_items(),
    }


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

    # Resync the entire customer topic into memory
    customer_consumer.topics()
    customer_consumer.seek_to_beginning()

    while not CUSTOMERS:
        update_customers(customer_consumer)
        time.sleep(0.5)

    # Generate orders forever
    while True:
        # Get any new/updated customers
        update_customers(customer_consumer)

        # Generate an order
        order = generate_order()
        producer.send("orders", order)
        print(order)

        time.sleep(random.randrange(5))
