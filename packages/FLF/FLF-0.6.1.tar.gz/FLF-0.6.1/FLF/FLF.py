import json
import uuid

import pika
from pika.exceptions import AMQPConnectionError, ProbableAuthenticationError

from FLF.exceptions import ProcedureExecutionException


class Store:
    def __init__(self, callback):
        self.store = {}
        self.callback = callback

    def add(self, key, name, value, status, call_procedure, reply_to, req_id):

        if not (req_id in self.store):
            self.store[req_id] = {"params": {}, "files": {}}

        if name == "params":
            self.store[req_id]["params"] = json.loads(value)
        else:
            self.store[req_id]["files"][name] = value

        if status == "finished":
            self.on_request_complete(self.store.pop(req_id), key, call_procedure, reply_to, req_id)

    def on_request_complete(self, params, key, call_procedure, reply_to, req_id):
        self.callback(params, key, call_procedure, reply_to, req_id)


def publish_response(channel, req_id, reply_to, correlation_id, response_to, response_value, params, files):
    # send params
    params_headers = {
        "request_status": "sending" if len(files.keys()) else "finished",
        "batch_name": "params",
        "req_id": req_id,
        response_to: response_value
    }
    params_properties = pika.BasicProperties(correlation_id=correlation_id, headers=params_headers)
    channel.basic_publish(exchange="", routing_key=reply_to, properties=params_properties, body=json.dumps(params))

    # send files
    for i, (file_name, file_content) in enumerate(files.items()):
        status = "finished" if len(files.keys()) - 1 == i else "sending"

        file_headers = {
            "request_status": status,
            "batch_name": file_name,
            "req_id": req_id,
            response_to: response_value
        }
        file_properties = pika.BasicProperties(correlation_id=correlation_id, headers=file_headers)
        channel.basic_publish(exchange="", routing_key=reply_to, properties=file_properties, body=file_content)


class InputStream:
    def __init__(self, channel, correlation_id, reply_to, params=None, files=None):
        if params is None:
            params = dict()
        self.params = params

        if files is None:
            files = dict()
        self.files = files

        self.correlation_id = correlation_id
        self.channel = channel
        self.reply_to = reply_to

    def send(self, response_id):
        req_id = str(uuid.uuid4())
        publish_response(self.channel, req_id, self.reply_to, self.correlation_id, "response_id", response_id,
                         self.params, self.files)


class OutputStream:
    def __init__(self, channel, correlation_id, reply_to, params=None, files=None):
        if params is None:
            params = dict()
        self.params = params

        if files is None:
            files = dict()
        self.files = files

        self.correlation_id = correlation_id
        self.channel = channel
        self.reply_to = reply_to

    def send(self, name, req_id):
        publish_response(self.channel, req_id, self.reply_to, self.correlation_id, "call_procedure", name,
                         self.params, self.files)


def create_connection(host, port, username, password):
    credentials = pika.PlainCredentials(username=username, password=password)
    connection_parameters = pika.ConnectionParameters(host=host, port=port, credentials=credentials)
    connection = pika.BlockingConnection(connection_parameters)

    return connection


class RpcServer:
    def __init__(self, host, port, username, password, procedures=None):
        self.host = host
        self.port = port
        self.username = username
        self.password = password

        if procedures is None:
            procedures = dict()

        self.procedures = procedures
        self.connection = None
        self.channel = None
        self.store = Store(self.on_complete_callback)

    def on_message(self, ch, method, props, body):
        request_status = props.headers["request_status"]
        batch_name = props.headers["batch_name"]
        correlation_id = props.correlation_id
        reply_to = props.reply_to
        call_procedure = props.headers["call_procedure"]
        req_id = props.headers["req_id"]

        # if server has needed procedure
        if call_procedure in self.procedures:
            self.on_request(request_status, batch_name, correlation_id, reply_to, call_procedure, body, req_id)
            self.channel.basic_ack(delivery_tag=method.delivery_tag)

    def on_complete_callback(self, params, key, call_procedure, reply_to, req_id):
        try:
            out, files = self.procedures[call_procedure](params["params"], params["files"])
            response = InputStream(self.channel, key, reply_to, json.dumps(out), files)
            response.send(req_id)
        except Exception as e:
            raise ProcedureExecutionException(f"Failed to execute procedure '{call_procedure}': {str(e)}")

    # код приема запроса
    def on_request(self, request_status, batch_name, correlation_id, reply_to, call_procedure, body, req_id):
        self.store.add(correlation_id, batch_name, body, request_status, call_procedure, reply_to, req_id)

    def connect(self):
        print("Rpc server connects to the queue server")

        try:
            return create_connection(self.host, self.port, self.username, self.password)
        except ProbableAuthenticationError:
            raise RuntimeError("Authorization error, code 1")
        except AMQPConnectionError:
            raise RuntimeError("Connection error, code 2")

    def create_req_channel(self, connection):
        print("Rpc server creates a channel")

        channel = connection.channel()
        channel.queue_declare(queue="rpc_queue")
        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(queue="rpc_queue", on_message_callback=self.on_message)
        self.channel = channel

    def listen(self):
        print("Listening")
        self.channel.start_consuming()

    def begin(self):
        while True:
            try:
                with self.connect() as connection:
                    self.create_req_channel(connection)
                    self.listen()
            except Exception as e:
                print("Exception:", str(e))


class RpcConnector:
    def __init__(self, host, port, username, password):
        self.host = host
        self.port = port
        self.username = username
        self.password = password

        self.connection = None
        self.channel = None
        self.callback_queue = None
        self.response = None
        self.correlation_id = str(uuid.uuid4())
        self.store = Store(self.on_complete_callback)

    def on_message(self, ch, method, props, body):
        correlation_id = props.correlation_id
        request_status = props.headers["request_status"]
        batch_name = props.headers["batch_name"]
        req_id = props.headers["req_id"]

        if self.correlation_id == correlation_id:
            print(body)
            self.on_response(request_status, batch_name, correlation_id, body, req_id)

    def on_complete_callback(self, params, key, call_procedure, reply_to, req_id):
        self.response = params

    def on_response(self, request_status, batch_name, correlation_id, body, req_id):
        self.store.add(correlation_id, batch_name, body, request_status, None, None, req_id)

    def call_procedure(self, name, params=None, files=None):
        try:
            self.response = None

            if params is None:
                params = dict()
            if files is None:
                files = dict()

            req_id = str(uuid.uuid4())

            request = OutputStream(self.channel, self.correlation_id, self.callback_queue, params, files)
            request.send(name, req_id)

            while self.response is None:
                self.connection.process_data_events()

            return self.response["params"], self.response["files"]
        except Exception as e:
            raise ProcedureExecutionException(f"Failed to execute procedure '{name}': {str(e)}")

    def connect(self):
        print("Rpc client connects to the queue server")

        try:
            return create_connection(self.host, self.port, self.username, self.password)
        except ProbableAuthenticationError:
            raise RuntimeError("Authorization error, code 1")
        except AMQPConnectionError:
            raise RuntimeError("Connection error, code 2")

    def create_channel(self):
        print("Rpc client creates the channel")

        self.channel = self.connection.channel()
        self.callback_queue = self.channel.queue_declare(queue="", exclusive=True).method.queue
        self.channel.basic_consume(queue=self.callback_queue, on_message_callback=self.on_message, auto_ack=True)

    def begin(self):
        self.connection = self.connect()
        self.create_channel()

