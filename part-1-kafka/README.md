# AWS Managed Streaming for Apache Kafka (MSK)

## Introduction to the Pub/Sub (Publish/Subscribe) Model

A way to get a message from A to B, C and D in a flexible, decoupled and resilient manner.

There are 3 basic primitives to understand in a Pub/Sub service:
* Topic (message store)
  * Collection of messages sent from published, destined to subscribers
  * A Topic usually holds messages of a similar schema, an interface contract between publishers and subscribers
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
  * Certain Pub/Sub implementations form clusters of brokers that 'share' a topic in a resilient and performant manner (eg. Kafka!)

## How does it fit together?

The flow of events in a Pub/Sub service usually follows these basic steps:
1. A Topic is created 
2. One or more subscribers 'register themselves' with the topic
3. A Publisher generates a piece of information
4. An event is sent to the Broker hosting the topic with the information
5. The Broker ensures the event is stored correctly and makes it available to its Subscribers
6. One or more Subscribers download the event and do 'something'
