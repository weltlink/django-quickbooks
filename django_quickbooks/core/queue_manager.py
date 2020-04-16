

class QueueManager:

    def get_message(self, queue_name, **kwargs):
        raise NotImplemented

    def publish_message(self, msg, queue_name, **kwargs):
        raise NotImplemented

    def get_message_count(self, queue_name):
        raise NotImplemented

    def delete(self, queue_name):
        raise NotImplemented

    def purge(self, queue_name):
        raise NotImplemented
