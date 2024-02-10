from locust import HttpUser, task, between
import time

# go to http://localhost:8089 to see the Locust dashboard, ( http://10.2.15.58:8089  wont work)

class MyUser(HttpUser):
    wait_time = between(1, 1)  # Time between requests # same as http_client.py think time
    host = 'http://10.2.7.109:8000'  # Host (server VM) and port

    @task
    def my_task(self):
        # Define your HTTP request here
        self.client.get(self.host + "/")
        # You can also mock responses or perform any other actions here
