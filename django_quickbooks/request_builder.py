class RequestBuilder:

    def __init__(self, queue_manager, request_queue_prefix=None):
        self.queue_manager = queue_manager

        if request_queue_prefix is None:
            request_queue_prefix = 'requests:realms:'

        self.request_queue_prefix = request_queue_prefix

    def process(self, realm_id, request_body):
        queue_name = '%s:%s' % (self.request_queue_prefix, realm_id)
        self.queue_manager.publish_message(request_body, queue_name)
