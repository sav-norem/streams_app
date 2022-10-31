import random
import redis
import time

# a basic consumer for testing that is now deprecated

STREAM_KEY = "jobs"

r = redis.Redis(decode_responses=True)

last_job_id = 0

while True:
    print("Checking for jobs...")
    response = r.xread(streams={STREAM_KEY: last_job_id}, block=5000)
    print(response)

    if len(response) == 0:
        print("Nothing to do right now, sleeping...")
        time.sleep(5)
    else:
        # r.xdel(STREAM_KEY, last_job_id)
        next_id = 0
        if len(response) > 1:
            next_job = response[1]
            next_id = next_job[1][0][0]
        job = response[0]
        print(job)
        current_job_id = job[1][0][0]
        current_job_details = job[1][0][1]
        print(f"Performing job {current_job_id}: {current_job_details}")
        time.sleep(15)
        last_job_id = current_job_id