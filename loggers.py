import logging

# get me a logger
logging.basicConfig(level=logging.DEBUG, format='[%(name)s] - %(message)s')
producer_logger = logging.getLogger('Producer')
consumer_logger = logging.getLogger("Consumer")

