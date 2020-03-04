# Intro to the two Kinesis offerings we'll be going through

# Kinesis Data Streams
Getting data from A to B.
Similar concept to a Kafka 'topic'.

Build script that will consume the various Kafka topics and pipe them into their respective kinesis streams


# Kinesis Data Analytics
Running analytical queries over your data stream
Many possible methods to aggregate and window


Pipe in the above Kinesis Data Streams into their Kinesis Data Analytics pipes

Generate some example SQL to go over the top and generate some insights!



# Deploy the AWS Kinesis Streams & Analytics
```bash
aws cloudformation deploy --template-file infrastructure-as-code/kinesis-streams.yml --stack-name streaming-<your-name>-kinesis-streams --parameter-overrides "ResourcePrefix=streaming-<your-name>" --capabilities CAPABILITY_IAM

# Example as Michael Robbins
aws cloudformation deploy --template-file infrastructure-as-code/kinesis-streams.yml --stack-name streaming-michaelr-kinesis-streams --parameter-overrides "ResourcePrefix=streaming-michaelr" --capabilities CAPABILITY_IAM
```
