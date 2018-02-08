__author__ = 'hand'

from kafka import KafkaProducer
from kafka import KafkaConsumer

class AITaskLog():
    #used to collect log to return to java side
    logRoller = {}
    def __init__(self,filename,kafka_settings):
        self.file_writer = None
        self.kafka_producer = None
        if filename:
            self.file_writer = open(filename,'a')
        if kafka_settings:
            # the default kafka producer settings is:
            # {
            #  'bootstrap_servers':'192.168.11.190:6667'
            #  topic:ai-userid-taskid
            # }
            self.kafka_producer = KafkaProducer(bootstrap_servers=kafka_settings.get('bootstrap_servers','192.168.11.190:6667'))
            self.default_kafka_topic = kafka_settings.get('topic','ai-unknown-user-unknown-task')

    def write(self,message):
        if self.file_writer:
            self.file_writer.write(message)

            #store the log message to correspond log roller
            orilogname = self.file_writer.__getattribute__('name')
            logname = orilogname.split('/')[-1]
            logroller = AITaskLog.logRoller.get(logname,'')
            logroller += message
            AITaskLog.logRoller[logname] = logroller
        if self.kafka_producer:
            my_bytes = bytes(message)
            self.kafka_producer.send(self.default_kafka_topic, value=my_bytes)

    def close(self):
        if self.file_writer:
            self.file_writer.close()

    def kafka_flush(self):
        if self.kafka_producer:
            self.kafka_producer.flush()


    def kafka_pop(self):
        if self.kafka_producer:
            consumer = KafkaConsumer('ai',group_id='my-group',bootstrap_servers=['172.29.1.6:6667'])
            for message in consumer:
                # message value and key are raw bytes -- decode if necessary!
                # e.g., for unicode: `message.value.decode('utf-8')`
                print ("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition,
                                                      message.offset, message.key,
                                                      message.value))
                # print(message.value)
    @staticmethod
    def kafka_send(kafka_producer,topic,value):
        kafka_producer.send(topic,value = bytes(value))

    @staticmethod
    def kafka_read(topic):
        consumer = KafkaConsumer(topic,group_id='my-group',bootstrap_servers=['172.29.1.6:6667'])
        for message in consumer:
            # message value and key are raw bytes -- decode if necessary!
            # e.g., for unicode: `message.value.decode('utf-8')`
            # print("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition,message.offset, message.key,message.value))
            print(message.value)
if __name__ == '__main__':
    # kafka_producer = KafkaProducer(bootstrap_servers = '192.168.11.190:6667')
    # AITaskLog.kafka_send(kafka_producer,'ai', 'hello')
    #
    # # AITaskLog.kafka_read()
    # kafka_producer.flush()
    AITaskLog.kafka_read('ai-unknown-user-unknown-task')
