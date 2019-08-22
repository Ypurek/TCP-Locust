# TCP Locust
 addon to make locust.io work with tcp sockets
 
 to test addon:
 1. Get locust.io  
 ```bash
 pip install locustio
 ```
 2. Run tcp server (it will run on port 8888)  
 ```bash
 python tcp_server
 ```
 3. Run locust with provided sample
```bash
 locust -f locustfile.py
 ```
 
 All configurations like host, port can be done in locustfile.  
 Socket client has only one function **send_bytes**  
 By default every response considered as successful. In case response need to be validated set attribute catch_response=True and handle:
 ```python
response = self.client.send_bytes(request_name='get yes', input=b'get yes', catch_response=True)
data = response.data.decode('utf-8')
    if data == 'yes':
        response.success()
    else:
        response.failure(f'response is {data}')
```          
## Important notes 
1. Response data received in bytes and need to be converted first
2. TCP client has dirty hack **time.sleep(1)** It is done to make sure complete response from server received. If you don't experience any issues just remove it
