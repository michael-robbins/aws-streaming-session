#!/usr/bin/env python3

from kafka import KafkaProducer
from kafka.errors import KafkaError
from common import get_brokers

import requests
import random
import json
import time


PROFILE_URL = "https://randomuser.me/api/?nat=au"


def generate_customer():
    response = requests.get(PROFILE_URL).json()
    profile = response["results"][0]

    return {
        "id": profile["id"]["value"],
        "first_name": profile["name"]["first"],
        "last_name": profile["name"]["last"],

        "location": profile["location"],

        "email": profile["email"],
        "login": profile["login"],
        "dob": profile["dob"],
        "phone": profile["phone"],
    }


if __name__ == "__main__":
    brokers = get_brokers()

    producer = KafkaProducer(
        bootstrap_servers=brokers,
        value_serializer=lambda m: json.dumps(m).encode("utf-8"),
    )

    while True:
        customer = generate_customer()
        producer.send("customers", customer)
        print(customer)

        time.sleep(random.randrange(10))
