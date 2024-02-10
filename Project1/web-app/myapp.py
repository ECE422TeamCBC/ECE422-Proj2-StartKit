
"""
A simple web application (modified); return the number of times it has been visited, and also the amount of time that took to
run the difficult function.
"""

from flask import Flask, request, g, Response
from redis import Redis
import random
import time
import requests

app = Flask(__name__)

redis = Redis(host='redis', port=6379, decode_responses=True)
# redis = Redis(host='10.2.7.109', port=6379)
list_key = 'timearray'
# startt

@app.before_request
def start_timer():
    # global start
    g.start = time.time()

def difficult_function():
    output = 1
    t0 = time.time()
    difficulty = random.randint(1000000, 2000000)
    for i in range(difficulty):
        output = output * difficulty
        output = output / (difficulty - 1)
    t1 = time.time()
    compute_time = t1 - t0
    return compute_time

@app.route('/')
def hello():
    # global startt
    start = time.time()
    redis.set('hits133', random.randint(1, 100))
    count = redis.incr('hits')
    computation_time = difficult_function()
    end = time.time()
    # responsetime = end - startt
    # redis.rpush('timearray', random.randint(1, 100))
    # redis.zadd('timearray', {end: end})  # Sorted Set for timestamps
    redis.incr('request_count')
    redis.incrbyfloat('request_time_sum', (end - start))

    request_sum = float(redis.get('request_time_sum'))
    request_count = int(redis.get('request_count'))
    if request_count >= 10:
        avg_request_time = request_sum / float(request_count)
        if avg_request_time > 7.0:
            redis.set('request_time_sum', 0)
            redis.set('request_count', 0)
            requests.post(url="http://10.2.7.109:5001/scaleup")
        elif avg_request_time < 4.0:
            redis.set('request_time_sum', 0)
            redis.set('request_count', 0)
            requests.post(url="http://10.2.7.109:5001/scaledown")

    redis.hset('datahash', 1, (end - g.start))  # Hash for values
    return 'Hello There! I have been seen {} times. I have solved the problem in {} seconds.\n'.format(count,
                                                                                                       computation_time)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
