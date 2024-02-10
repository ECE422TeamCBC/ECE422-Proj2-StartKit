from redis import Redis
import time

interval = 10
buffer_size = 3

redis = Redis(host='redis', port=6379)

def get_hits():
    return int(redis.get('hits') or 0)

def calculate_average(buffer):
    return sum(buffer) / len(buffer) if len(buffer) > 0 else 0

def set_hitsAvg10sOver30s(hitsAvg10sOver30s):
    redis.set('hitsAvg10sOver30s', hitsAvg10sOver30s)

def main():
    hits_buffer = [0] * buffer_size
    buffer_index = 0

    while True:
        time.sleep(interval)
        current_hits = get_hits()
        hits_change = current_hits - hits_buffer[buffer_index]
        print(f"Hits change in the last {interval} seconds: {hits_change}")
        hits_buffer[buffer_index] = hits_change
        buffer_index = (buffer_index + 1) % buffer_size

        hitsAvg10sOver30s = calculate_average(hits_buffer)
        print(f"Average hits in the last {buffer_size * interval} seconds: {hitsAvg10sOver30s}")
        set_hitsAvg10sOver30s(hitsAvg10sOver30s)

if __name__ == "__main__":
    main()