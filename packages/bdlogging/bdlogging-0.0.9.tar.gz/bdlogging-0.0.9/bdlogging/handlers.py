import logging.handlers
import pika
import os
from pika.adapters.blocking_connection import BlockingConnection, BlockingChannel
import json


def get_logging_level():
    loglevel = int(os.environ.get('loglevel', 0))
    level = logging.INFO
    if loglevel == 0:
        level = logging.DEBUG
    elif loglevel == 1:
        level = logging.INFO
    elif loglevel == 2:
        level = logging.WARNING
    elif loglevel == 3:
        level = logging.ERROR
    elif loglevel == 4:
        level = logging.CRITICAL
    else:
        level = logging.INFO
    return level


class RabbitMQHandler(logging.Handler):

    def __init__(self, level=None):

        if not level:
            level = get_logging_level()

        super().__init__(level)
        fmt = ('%(asctime)s$$%(levelname)s$$%(name)s$$%(threadName)s$$'
               '%(module)s.%(funcName)s:%(lineno)4d$$%(message)s')
        fmt = logging.Formatter(fmt, None, "%")
        self.setFormatter(fmt)

        self.rabbithost = os.environ.get('rabbithost', 'localhost')
        self.rabbitport = int(os.environ.get('rabbitport', 5672))
        self.connection: pika.BlockingConnection = None
        self.channel: BlockingChannel = None
        self.exchange = "logs"
        self.open_connection()
        self.createLock()

    def open_connection(self):
        try:
            if not self.connection or self.connection.is_closed:
                self.connection = pika.BlockingConnection(
                    pika.ConnectionParameters(host=self.rabbithost, port=self.rabbitport))
            self.channel = self.connection.channel()
            self.channel.exchange_declare(
                exchange=self.exchange, exchange_type="topic", durable=True, auto_delete=False)
            return True
        except:
            self.connection = None
            self.channel = None
            return False

    def close_connection(self):
        if self.channel and not self.channel.is_closed:
            self.channel.close()

        if self.connection and not self.connection.is_closed:
            self.connection.close()

        self.connection, self.channel = None, None

    def emit(self, record):
        try:
            openflg = True
            self.acquire()
            if not self.connection or self.connection.is_closed or not self.channel or self.channel.is_closed:
                openflg = self.open_connection()
            if openflg:
                routing_key = record.levelname
                formatted = self.format(record)
                formatted = formatted.split('$$')
                json_data = {
                    'time': formatted[0],
                    'level': formatted[1],
                    'logname': formatted[2],
                    'threadname': formatted[3],
                    'modulename': formatted[4],
                    'message': formatted[5]
                }

                self.channel.basic_publish(
                    exchange=self.exchange, routing_key=routing_key, body=json.dumps(json_data))
        except Exception:
            self.connection, self.channel = None, None
            # self.handleError(record)
        finally:
            self.release()

    def close(self):
        self.acquire()

        try:
            self.close_connection()
        finally:
            self.release()

    def __del__(self):
        self.close()
