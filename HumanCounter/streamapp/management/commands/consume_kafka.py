import json
from confluent_kafka import Consumer, KafkaException, KafkaError
from django.core.management.base import BaseCommand
from streamapp.models import EntryExitCount

class Command(BaseCommand):
    help = 'Consumes Kafka messages and updates the database'

    def handle(self, *args, **options):
        conf = {
            'bootstrap.servers': 'localhost:9092',
            'group.id': 'entry_exit_counter_group',
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
                        self.stdout.write(self.style.ERROR(f'Error: {msg.error()}'))
                        continue
                try:
                    data = json.loads(msg.value().decode('utf-8'))
                    self.stdout.write(self.style.SUCCESS(f'Received message: {data}'))
                    entry_count = data.get('Entry', 0)
                    exit_count = data.get('Exit', 0)

                    for _ in range(entry_count):
                        EntryExitCount.objects.create(type='Entry')
                    for _ in range(exit_count):
                        EntryExitCount.objects.create(type='Exit')

                    self.stdout.write(self.style.SUCCESS(f'Entries added: {entry_count}, Exits added: {exit_count}'))
                except json.JSONDecodeError as e:
                    self.stdout.write(self.style.ERROR(f'JSON decode error: {e} - Raw message: {msg.value()}'))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Unexpected error: {e}'))
        finally:
            
            consumer.close()
