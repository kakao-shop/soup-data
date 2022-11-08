from kafka import KafkaConsumer
from json import loads
from time import sleep
# topic, broker list
consumer = KafkaConsumer(
    'test',
     bootstrap_servers=['localhost:9092'],
     auto_offset_reset='earliest',
     enable_auto_commit=True,
     group_id='my-group',
     consumer_timeout_ms=1000
)

# consumer list를 가져온다
print('[begin] get consumer list')
while True:
    for message in consumer:
        if message == None: sleep(1)
        print(message)
print('[end] get consumer list')