from redis import Redis
import time

interval = 10
index_size = 20

redis = Redis(host='10.2.7.109', port=6379)
list_key = 'timearray'
avglist_key = 'atimearray'

def calculate_average(buffer):
    return sum(buffer) / len(buffer) if len(buffer) > 0 else 0

def set_AvgOver(atimearray):
    redis.rpush(avglist_key, atimearray)

def main():

    while True:
        time.sleep(interval)
        stored_array = redis.lrange(list_key, 0, -1)
        avgoftimearray = 0
        if (len(stored_array) >= index_size ):
            stored_array = stored_array[-index_size:]
            avgoftimearray = calculate_average(stored_array)
            print("Length of the array:", len(stored_array))
            print(" ".join(map(str, stored_array)))
            print(f"Average: {avgoftimearray}")
            set_AvgOver(avgoftimearray)
        else:
            avgoftimearray = calculate_average(stored_array)
            print("Length of the array:", len(stored_array))
            print(" ".join(map(str, stored_array)))
            print(f"Average: {avgoftimearray}")
            set_AvgOver(avgoftimearray)


if __name__ == "__main__":
    main()