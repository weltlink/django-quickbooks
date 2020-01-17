from abc import abstractmethod


class QueueManager:

    @abstractmethod
    def get_message(self, queue_name, ack=True):
        pass

    @abstractmethod
    def publish_message(self, msg, queue_name, delete_queue=False):
        pass

    @abstractmethod
    def get_queue_message_count(self, queue_name):
        pass

    @abstractmethod
    def delete_queue(self, queue_name):
        pass

    @abstractmethod
    def purge_queue(self, queue_name):
        pass
