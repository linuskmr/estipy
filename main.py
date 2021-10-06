import time
from eta import ETA

# Some data to be processed
data = list(range(42))

for num, _ in ETA(data):
    # Do something useful here that takes a little time
    print(num)
    time.sleep(0.1)
