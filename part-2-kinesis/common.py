import json
import os


DEFAULT_BROKERS = [
    "broker-1:9092",
    "broker-2:9092",
    "broker-3:9092",
]


def get_prefix(filename="../resource_prefix.json"):
    if not os.path.exists(prefix_filename):
        return None

    with open(prefix_filename) as prefix_file:
        prefix = json.load(prefix_file)["prefix"]


def get_brokers():
    prefix = get_prefix()

    if prefix is None:
        return DEFAULT_BROKERS

    import boto3
    msk = boto3.client("kafka")

    response = msk.list_clusters(ClusterNameFilter=prefix)
    cluster_arn = response["ClusterInfoList"][0]["ClusterArn"]

    response = msk.get_bootstrap_brokers(ClusterArn=cluster_arn)
    brokers = response["BootstrapBrokerString"].split(",")

    return brokers
