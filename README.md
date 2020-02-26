# AWS Streaming Session
AWS Streaming Walkthrough of Kinesis &amp; Kafka

This session will be broken into two parts:
Part 1: AWS Managed Streaming for Apache Kafka (MSK)
Part 2: AWS Kinesis (Streams & Analytics)


Part 1: AWS Managed Streaming for Apache Kafka (MSK)
- Basic intro into Kafka, Pub & Sub, Different Mindset
- Have a few ‘data producers’ pre built and running?
- We’ll provision an AWS Managed Kafka cluster
- Create 3 topics
- Provision 4 scripts (Data Producer #1 & #2, Data Consumer #1 & #2)
- Data Producer #1 => Topic #1
- Data Producer #2 => Topic #2
- Data Consumer #1 (Topic #1 & Topic #2) => Topic #3
- Data Consumer #2 (Topic #3) => AWS S3


Part 2: AWS Kinesis Streams & Analytics
- Differences from Kafka to Kinesis
- Data Consumer #2 (Topic #3) => Kinesis Data Stream
- Kinesis Data Stream => Kinesis Data Analytics (Insights) => S3?
