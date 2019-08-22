import time, socket
from locust import Locust, events, exception


class TcpSocketClient:
    buff_size = None
    host = None
    port = None

    def __init__(self, host, port, buff_size=4096):
        self.host = host
        self.port = port
        self.buff_size = buff_size

    def __get_data(self, host: str, port: int, input: bytes, buff_size: int):
        data = b''
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))
            s.sendall(input)
            while True:
                part = s.recv(buff_size)
                time.sleep(1)
                data += part
                if len(part) < buff_size:
                    return data

    def send_bytes(self, request_name: str, input: bytes, catch_response=False):
        start_time = time.time()
        data = self.__get_data(host=self.host, port=self.port, input=input, buff_size=self.buff_size)
        response_time = (time.time() - start_time) * 1000
        content_size = len(data)
        if not catch_response:
            events.request_success.fire(
                request_type='SEND BYTES',
                name=request_name,
                response_time=response_time,
                response_length=content_size,
            )
        return TcpSocketResponse({'type': 'SEND BYTES',
                                  'name': request_name,
                                  'time': response_time,
                                  'length': content_size,
                                  'bytes': data})


class TcpSocketResponse:
    details = None
    request_name = None
    response_time = None
    content_length = None
    data = None

    def __init__(self, request_details):
        self.details = request_details
        self.request_name = request_details['name']
        self.response_time = request_details['time']
        self.content_length = request_details['length']
        self.data = request_details['bytes']

    def success(self):
        events.request_success.fire(
            request_type=self.details['type'],
            name=self.details['name'],
            response_time=self.details['time'],
            response_length=self.details['length']
        )

    def failure(self, message):
        events.request_failure.fire(
            request_type=self.details['type'],
            name=self.details['name'],
            response_time=self.details['time'],
            exception=message
        )


class TcpSocketLocust(Locust):
    client = None
    port = None
    buff_size = 4096

    def __init__(self):
        super(TcpSocketLocust, self).__init__()
        if self.host is None or self.port is None:
            raise exception.LocustError(
                "You must specify the base host and port. Either in the host attribute in the Locust class, or on the command line using the --host --port options.")
        self.client = TcpSocketClient(self.host, self.port, self.buff_size)
