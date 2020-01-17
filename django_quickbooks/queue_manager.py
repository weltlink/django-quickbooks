import logging

import pika
from pika import BlockingConnection, ConnectionParameters, PlainCredentials
from pika.adapters.blocking_connection import BlockingChannel

from django_quickbooks.core.queue_manager import QueueManager
from django_quickbooks.settings import qbwc_settings


class RabbitMQManager(QueueManager):
    def __init__(self):
        self._connection = None
        self._input_channel = None
        self._output_channel = None

    def _get_channel(self, receive=True) -> BlockingChannel:
        if receive:
            if hasattr(self, '_input_channel') and self._input_channel and self._input_channel.is_open:
                return self._input_channel

            self._input_channel = self._get_connection().channel()
            return self._input_channel
        else:
            if hasattr(self, '_output_channel') and self._output_channel and self._output_channel.is_open:
                return self._output_channel

            self._output_channel = self._get_connection().channel()
            return self._output_channel

    def _get_connection(self) -> BlockingConnection:
        if hasattr(self, '_connection') and self._connection and self._connection.is_open:
            return self._connection
        self._connection = BlockingConnection(
            ConnectionParameters(
                host=qbwc_settings.RABBITMQ_DEFAULT_HOST,
                virtual_host=qbwc_settings.RABBITMQ_DEFAULT_VHOST,
                credentials=PlainCredentials(
                    username=qbwc_settings.RABBITMQ_DEFAULT_USER,
                    password=qbwc_settings.RABBITMQ_DEFAULT_PASS
                ),
                heartbeat=600,
                blocked_connection_timeout=300,
                connection_attempts=1000,
            )
        )

        return self._connection

    def get_message(self, queue_name, ack=True):
        channel = self._get_channel()
        method_frame, header_frame, body = channel.basic_get(str(queue_name))
        if method_frame:
            if ack:
                self._get_channel().basic_ack(method_frame.delivery_tag)
            return body if isinstance(body, str) else body.decode('UTF-8') if isinstance(body, bytes) else body
        else:
            logging.error("No request in the queue, error.")
            return ""

    def publish_message(self, msg, queue_name, delete_queue=False):
        queue_name = str(queue_name)
        channel = self._get_channel(receive=False)
        if delete_queue:
            channel.queue_delete(queue_name)
        channel.queue_declare(queue_name, arguments={'x-queue-mode': 'lazy', 'x-max-length': 1000})
        channel.basic_publish(exchange='', routing_key=queue_name, body=msg, properties=pika.BasicProperties(
            delivery_mode=2  # persistent
        ))

    def get_queue_message_count(self, queue_name):
        return self._get_channel().queue_declare(
            queue=queue_name,
            arguments={'x-queue-mode': 'lazy', 'x-max-length': 1000}
        ).method.message_count

    def delete_queue(self, queue_name):
        self._get_channel().queue_delete(queue=queue_name)

    def purge_queue(self, queue_name):
        self._get_channel().queue_purge(queue=queue_name)
