import json
from confluent_kafka import Consumer, KafkaException
from django.core.management.base import BaseCommand
from streamapp.models import EntryExitCount

class Command(BaseCommand):
    help = 'Consumes Kafka messages and updates the database'

    def handle(self, *args, **options):
        conf = {
            'bootstrap.servers': 'localhost:9092',
            'group.id': 'my_group',
            'auto.offset.reset': 'earliest',
        }
        consumer = Consumer(conf)

        consumer.subscribe(['your_kafka_topic'])

        try:
            while True:
                msg = consumer.poll(timeout=1.0)
                if msg is None:
                    continue
                if msg.error():
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                        continue
                    else:
                        raise KafkaException(msg.error())
                data = json.loads(msg.value().decode('utf-8'))
                if 'entry' in data:
                    EntryExitCount.objects.create(type='Entry')
                    self.stdout.write(self.style.SUCCESS('Entry added'))
                elif 'exit' in data:
                    EntryExitCount.objects.create(type='Exit')
                    self.stdout.write(self.style.SUCCESS('Exit added'))
                else:
                    self.stdout.write(self.style.WARNING('Unknown message type'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error: {str(e)}'))
        finally:
            consumer.close()
