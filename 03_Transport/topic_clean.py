from confluent_kafka import Consumer, KafkaError

c = Consumer({
    'bootstrap.servers': 'pkc-lgk0v.us-west1.gcp.confluent.cloud:9092',
    'group.id': 'my-group',
    'auto.offset.reset': 'earliest'
})

c.subscribe(['my-topic'])

while True:
    msg = c.poll(1.0)

    if msg is None:
        continue
    if msg.error():
        if msg.error().code() == KafkaError._PARTITION_EOF:
            print('End of partition reached')
        else:
            print('Error while consuming message: {}'.format(msg.error()))
    else:
        print('Received message: {}'.format(msg.value()))

c.close()
