#!/usr/bin/env python3

from kafka import KafkaProducer
from kafka.errors import KafkaError

import datetime
import random
import json
import time


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

def generate_items(choices=3):
    return [random.choice(PRODUCTS) for _ in range(random.randrange(1, choices + 1))]

def generate_order(order_id):
    return {
        "order_id": order_id,
        "order_time": datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S%z"),
        "items": generate_items(),
    }

def send_items_forever(producer, topic):
    order_id = 100001

    while True:
        order = generate_order(order_id)
        producer.send(topic, key=str(order_id).encode("utf-8"), value=order)
        print(order)
        order_id += 1

        time.sleep(random.randrange(5))

if __name__ == "__main__":
    brokers = [
        "broker-1:9092",
        "broker-2:9092",
        "broker-3:9092"
    ]

    producer = KafkaProducer(
        bootstrap_servers=brokers,
        value_serializer=lambda m: json.dumps(m).encode('utf-8'),
    )

    send_items_forever(producer, "orders")
