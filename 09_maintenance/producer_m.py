#!/usr/bin/env python















import sys



import json

import time 







from random import choice







from argparse import ArgumentParser, FileType







from configparser import ConfigParser







from confluent_kafka import Producer















if __name__ == '__main__':







    # Parse the command line.







    parser = ArgumentParser()







    parser.add_argument('config_file', type=FileType('r'))







    parser.add_argument('json_file', type=str)







    args = parser.parse_args()















    # Parse the configuration.







    # See https://github.com/edenhill/librdkafka/blob/master/CONFIGURATION.md







    config_parser = ConfigParser()







    config_parser.read_file(args.config_file)







    config = dict(config_parser['default'])















    # Create Producer instance







    producer = Producer(config)















    # Optional per-message delivery callback (triggered by poll() or flush())







    # when a message has been successfully delivered or permanently







    # failed delivery (after retries).







    def delivery_callback(err, msg):







        if err:







            print('ERROR: Message failed delivery: {}'.format(err))







        else:







            print("Produced event to topic {topic}: key = {key:12} value = {value:12}".format(







                topic=msg.topic(), key=msg.key().decode('utf-8'), value=msg.value().decode('utf-8')))















    with open(args.json_file, 'r') as json_file:







        data_json = json.load(json_file)







    # Produce data by selecting random values from these lists.







    topic = "archivetest"







    len_of_json = len(data_json)







    for i in range(len_of_json):



        value = json.dumps(data_json[i])

        producer.produce(topic, value, str(i), callback=delivery_callback)

        #time.sleep(0.25)







    # Block until the messages are sent.







    producer.poll(10000)







    producer.flush()