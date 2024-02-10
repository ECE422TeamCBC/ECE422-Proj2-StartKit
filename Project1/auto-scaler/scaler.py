
"""
A simple web application; return the number of time it has been visited and also the amount of time that took to
run the difficult function.
"""

from flask import Flask, request
import subprocess
from redis import Redis

app = Flask(__name__)
redis = Redis(host='redis', port=6379)
redis.incr("num_replicas")

@app.route('/scaleup', methods=['POST'])
def scale():
    redis.incr("num_replicas")
    subprocess.run(["bash", "./scale.sh", "app_name_web", "scaleup"])
    return '', 200

@app.route('/scaledown', methods=['POST'])
def scale_down():
    redis.decr("num_replicas")
    subprocess.run(["bash", "./scale.sh", "app_name_web", "scaledown"])
    return '', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
