import argparse

from FLF import RpcConnector


def main():
    parser = argparse.ArgumentParser(description="Example RPCServer for RabbitMQ")
    parser.add_argument("--host", default="localhost", type=str, help="host")
    parser.add_argument("--port", default=5672, type=int, help="port")
    parser.add_argument("--username", default="rabbitmq", type=str, help="username")
    parser.add_argument("--password", default="rabbitmq", type=str, help="password")
    args = parser.parse_args()

    connector = RpcConnector(host=args.host, port=args.port, username=args.username, password=args.password)
    connector.begin()

    file_bytes = b"hello, this is a file"
    print(connector.call_procedure("addition", {"a": 22, "b": 33}, {"file": file_bytes}))
    print(connector.call_procedure("multiply", {"a": 33, "b": 33}, {"file": file_bytes}))
    print(connector.call_procedure("addition", {"a": 234, "b": 33}, {"file": file_bytes}))
    print(connector.call_procedure("multiply", {"a": 22, "b": 33}, {"file": file_bytes}))
    print(connector.call_procedure("unknown4real"))


if __name__ == "__main__":
    main()

