# Intro to the two AWS Kinesis offerings we'll be going through

## AWS Kinesis Data Streams
A way to get a message from A to B, C and/or D in a highly scalable, decoupled, resilient 'pipe'.

Similar concept to a Kafka 'topic', with all the underlying tweaks to scale out, order, group your messages to ensure they're read correctly by your consumers.

While messages in Kafka can potentially be stored forever, Kinesis Data Streams are more focused around being that 'pipe' that provides transport for messages, not being your final storage.

## AWS Kinesis Data Analytics
Provides the ability to consume a stream of data (Kinesis Firehose, Kinesis Streams, other producers as well) and run an 'application' (SQL Dialect or Apache Flink) over the stream.

Similar concept to KSQL that was mentioned in Part 1 of the Streaming Session.

The built-in SQL dialect can run a number of analytical queries over the data, aggregating over windows, creating new metrics, and handle exporting to any supported output (other Kinesis Streams, Kinesis Firehose, Lambda).

## AWS Kinesis Firehose
We won't cover this in this session, but the main gist of Firehose is consuming streaming data and loading it into Data Lakes, Data Warehouses, S3, etc...

# Deploy the AWS Kinesis Streams & Analytics
```bash
aws cloudformation deploy --template-file infrastructure-as-code/kinesis-streams.yml --stack-name streaming-<your-name>-kinesis-streams --parameter-overrides "ResourcePrefix=streaming-<your-name>" --capabilities CAPABILITY_IAM

# Example as Michael Robbins
aws cloudformation deploy --template-file infrastructure-as-code/kinesis-streams.yml --stack-name streaming-michaelr-kinesis-streams --parameter-overrides "ResourcePrefix=streaming-michaelr" --capabilities CAPABILITY_IAM
```

# Further
1. Let's create another stream for another Kafka Index!
