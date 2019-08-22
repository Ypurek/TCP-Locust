from locust import TaskSet, task
from tcpSocketClient import TcpSocketLocust

ENCODING = 'utf-8'


class UserBehavior(TaskSet):
    @task(3)
    def test_default(self):
        self.client.send_bytes(request_name='hello world', input=b'hello')

    @task(1)
    def test_failures(self):
        response = self.client.send_bytes(request_name='get yes', input=b'get yes', catch_response=True)
        data = response.data.decode('utf-8')
        if data == 'yes':
            response.success()
        else:
            response.failure(f'response is {data}')


class WebsiteUser(TcpSocketLocust):
    host = 'localhost'
    port = 8888
    buff_size = 128
    task_set = UserBehavior
    min_wait = 1000
    max_wait = 2000
