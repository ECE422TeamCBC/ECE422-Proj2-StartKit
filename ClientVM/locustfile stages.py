
# go to http://localhost:8089 to see the Locust dashboard, ( http://10.2.15.58:8089  wont work)

from locust import HttpUser, LoadTestShape, TaskSet, constant, task
import time # 


class UserTasks(TaskSet):
    @task
    def get_root(self):
        self.client.get(self.user.host + "/") # Define your HTTP request here


class WebsiteUser(HttpUser):
    wait_time = constant(1) # same as http_client.py think time
    tasks = [UserTasks]
    host = "http://10.2.7.109:8000"  # Specify the base host


class StagesShape(LoadTestShape):
    """
    A simply load test shape class that has different user and spawn_rate at
    different stages.

    Keyword arguments:

        stages -- A list of dicts, each representing a stage with the following keys:
            duration -- When this many seconds pass the test is advanced to the next stage
            users -- Total user count
            spawn_rate -- Number of users to start/stop per second
            stop -- A boolean that can stop that test at a specific stage

        stop_at_end -- Can be set to stop once all stages have run.
    """

    stages = [
        {"duration": 60, "users": 60, "spawn_rate": 1}, # ramps up to 60 users, at 1 user/sec
        {"duration": 120, "users": 60, "spawn_rate": 1}, # Maintain peak users for 60sec
        {"duration": 180, "users": 120, "spawn_rate": 2}, # ramps up to 120 users, at 2 user/sec
        {"duration": 240, "users": 120, "spawn_rate": 2}, # Maintain peak users for 60sec
        {"duration": 300, "users": 180, "spawn_rate": 3}, # ramps up to 180 users, at 3 user/sec
        {"duration": 360, "users": 180, "spawn_rate": 3},  # Maintain peak users for 60sec
        {"duration": 420, "users": 120, "spawn_rate": 2}, # ramps down to 120 users, at 2 user/sec
        {"duration": 480, "users": 120, "spawn_rate": 2}, # Maintain peak users for 60sec
        {"duration": 540, "users": 60, "spawn_rate": 1}, # ramps down to 60 users, at 12 user/sec
        {"duration": 600, "users": 60, "spawn_rate": 1} # Maintain peak users for 60sec
    ]

    def tick(self):
        run_time = self.get_run_time()

        for stage in self.stages:
            if run_time < stage["duration"]:
                tick_data = (stage["users"], stage["spawn_rate"])
                return tick_data

        return None