#!/usr/bin/env python3

from common import get_prefix

import boto3


prefix = get_prefix()

if prefix is None:
    raise Exception("Unable to find prefix?")

streams = {
    "{prefix}-customer-stream".format(prefix=prefix): {},
}


kinesis = boto3.client("kinesis")

# Setup
for stream_name in streams.keys():
    response = kinesis.list_shards(
        StreamName=stream_name
    )

    shard = response["Shards"][0]

    streams[stream_name]["shard_id"] = shard["ShardId"]

while True:
    for stream_name, stream_options in streams.items():
        if not stream_options["iterator"]:
            response = client.get_shard_iterator(
                StreamName=stream_name,
                ShardId=stream_options["shard_id"],
                ShardIteratorType="TRIM_HORIZON",
            )

            stream_options["iterator"] = response["ShardIterator"]

        response = kinesis.get_records(
            ShardIterator=iterator,
            Limit=1,
        )

        print(response)

        for record in response["Records"]:
            print(record["Data"].decode("utf-8"))

        if response["NextShardIterator"]:
            stream_options["iterator"] = response["NextShardIterator"]
