import logging

from django_quickbooks.core.queue_manager import QueueManager
from django_quickbooks.settings import qbwc_settings


class RedisManager(QueueManager):
    def __init__(self, prefix=None, host=None, port=None, db=None, password=None):
        self._prefix = prefix or 'django_quickbooks'
        self._connection_host = host or qbwc_settings.REDIS_DEFAULT_HOST
        self._connection_port = port or qbwc_settings.REDIS_DEFAULT_PORT
        self._connection_db = db or qbwc_settings.REDIS_DEFAULT_DB
        self._connection_password = password or qbwc_settings.REDIS_DEFAULT_PASSWORD
        self._connection = None

    def _get_connection(self):
        from redis import Redis
        if not self._connection:
            self._connection = Redis(
                host=self._connection_host, port=self._connection_port, db=self._connection_db,
                password=self._connection_password
            )
        return self._connection

    def get_message(self, queue_name, **kwargs):
        conn = self._get_connection()
        return conn.lpop('%s:%s' % (self._prefix, queue_name))

    def publish_message(self, msg, queue_name, delete_queue=False):
        conn = self._get_connection()
        if delete_queue:
            self.delete(queue_name)
        conn.lpush('%s:%s' % (self._prefix, queue_name), msg)

    def get_message_count(self, queue_name):
        conn = self._get_connection()
        return conn.llen('%s:%s' % (self._prefix, queue_name))

    def delete(self, queue_name):
        conn = self._get_connection()
        redis_queue_name = '%s:%s' % (self._prefix, queue_name)
        for i in range(0, conn.llen(redis_queue_name)):
            conn.lpop(redis_queue_name)

    def purge(self, queue_name):
        self.delete(queue_name)


#  FIXME: Deprecated. RabbitMQManager is not optimized for keeping robust connection, use RedisManager as alternative
class RabbitMQManager(QueueManager):
    def __init__(self, host=None, virtual_host=None, username=None, password=None, **kwargs):
        self._connection_host = host or qbwc_settings.RABBITMQ_DEFAULT_HOST
        self._connection_virtual_host = virtual_host or qbwc_settings.RABBITMQ_DEFAULT_VHOST
        self._connection_username = username or qbwc_settings.RABBITMQ_DEFAULT_USER
        self._connection_password = password or qbwc_settings.RABBITMQ_DEFAULT_PASS
        self._connection = None
        self._input_channel = None
        self._output_channel = None
        super(RabbitMQManager, self).__init__(**kwargs)

    def _get_channel(self, receive=True):
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

    def _get_connection(self):
        from pika import BlockingConnection, ConnectionParameters, PlainCredentials

        if hasattr(self, '_connection') and self._connection and self._connection.is_open:
            return self._connection
        self._connection = BlockingConnection(
            ConnectionParameters(
                host=self._connection_host,
                virtual_host=self._connection_virtual_host,
                credentials=PlainCredentials(
                    username=self._connection_username,
                    password=self._connection_password
                ),
                heartbeat=100,
                blocked_connection_timeout=300,
                connection_attempts=4,
            )
        )

        return self._connection

    def get_message(self, queue_name, ack=True, **kwargs):
        channel = self._get_channel()
        method_frame, header_frame, body = channel.basic_get(str(queue_name))
        if method_frame:
            if ack:
                self._get_channel().basic_ack(method_frame.delivery_tag)
            return body if isinstance(body, str) else body.decode('UTF-8') if isinstance(body, bytes) else body
        else:
            logging.error("No request in the queue, error.")
            return ""

    def publish_message(self, msg, queue_name, delete_queue=False, **kwargs):
        from pika import BasicProperties

        queue_name = str(queue_name)
        channel = self._get_channel(receive=False)
        if delete_queue:
            channel.queue_delete(queue_name)
        channel.queue_declare(queue_name, arguments={'x-queue-mode': 'lazy', 'x-max-length': 1000})
        channel.basic_publish(exchange='', routing_key=queue_name, body=msg, properties=BasicProperties(
            delivery_mode=2  # persistent
        ))

    def get_message_count(self, queue_name):
        return self._get_channel().queue_declare(
            queue=queue_name,
            arguments={'x-queue-mode': 'lazy', 'x-max-length': 1000}
        ).method.message_count

    def delete(self, queue_name):
        self._get_channel().queue_delete(queue=queue_name)

    def purge(self, queue_name):
        self._get_channel().queue_purge(queue=queue_name)
