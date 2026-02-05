import time
from functools import wraps

# A global accumulator to track total time spent in your finder
TOTAL_TIME_NS = 0
CALL_COUNT = 0

def timeit(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        global TOTAL_TIME_NS, CALL_COUNT
        start = time.perf_counter_ns()
        result = func(*args, **kwargs)
        end = time.perf_counter_ns()
        
        TOTAL_TIME_NS += (end - start)
        CALL_COUNT += 1
        print(f"time: {TOTAL_TIME_NS/1000/1000:.2f} ms; called: {CALL_COUNT}")
        return result
    return wrapper
