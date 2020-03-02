# AWS Managed Streaming for Apache Kafka (MSK)

## Introduction to the Pub/Sub (Publish/Subscribe) Model

A way to get a message from A to B, C and/or D in a flexible, decoupled and resilient manner.

There are 3 basic primitives to understand in a Pub/Sub service:
* Topic (message store)
  * Collection of messages sent from publishers, destined to subscribers
  * Topics usually holds messages of a similar schema, an interface contract between publishers and subscribers
    * But this is not usually enforced by the Topic

* Publisher (message producer)
  * Publishers generate events (information) and send them to their pre-determined topics
  * A publisher can generate events for many topics

* Subscriber (message consumer)
  * Subscribers listen to one or more topics, receiving messages published on them
  * Subscribers don't need to know the publisher of the message, only the schema of it

Other parts of a Pub/Sub system include:
* Brokers
  * These are servers that 'host' a topic, or part thereof
  * Certain Pub/Sub implementations form clusters of brokers that 'share' a topic between nodes in a resilient and performant manner (eg. Kafka!)

* Shards
  * A 'part' of a topic, usually whos length is defined as a period of time
  * Stores messages for just that 'part', can be replicated/duplicated as nessesary
  * Multiple shards form a topic (not just specific to Kafka, AWS Kinesis has this concept as well!)

## How does it fit together?

The flow of events in a Pub/Sub service usually follows these basic steps:
1. A Topic is created
2. One or more subscribers 'register themselves' with the topic
3. A Publisher generates a piece of information
4. An event is sent to the Broker hosting the topic with the information
5. The Broker ensures the event is stored correctly and makes it available to its Subscribers
6. One or more Subscribers download the event and do 'something'

# Deploy the AWS Kafka Cluster

```bash
aws cloudformation deploy --template-file infrastructure-as-code/kafka-cluster.yml --stack-name streaming-<your-name>-kafka-cluster --parameter-overrides "ResourcePrefix=streaming-<your-name>"

# Example as Michael Robbins
aws cloudformation deploy --template-file infrastructure-as-code/kafka-cluster.yml --stack-name streaming-michaelr-kafka-cluster --parameter-overrides "ResourcePrefix=streaming-michaelr"
```

This will take approx. 10 minutes to deploy the Kafka cluster!
