from django_quickbooks.queue_manager import RabbitMQManager


class RequestBuilder(RabbitMQManager):

    def process(self, realm_id, request_body):
        self.publish_message(request_body, realm_id)
        self._get_channel().close()
        self._get_connection().close()


