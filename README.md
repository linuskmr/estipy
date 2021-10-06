# estipy

Estimate time of availability of long running for loops.

## Usage

```python
import time
from estipy.eta import ETA

# Some data to be processed
data = list(range(42))

for num, _ in ETA(data):
    # Do something useful here that takes a little time
    time.sleep(0.1)

# Example output:
# 13/42 = 31.0%, ETA Delta 0:00:02.685864, ETA 2021-07-04 14:50:12.486002
```

[Try it online](https://replit.com/@linuskmr/estipyexamples)

Or disable auto print and access all eta data

```python
for num, eta in ETA(data, auto_print=False):
    # Do something useful here that takes a little time
    time.sleep(0.1)
    print(eta.json(indent='  '))

# Example output:
# {
#   "total": {
#     "time": "0:00:03.762402",
#     "absolute": 42,
#     "percentage": 100
#   },
#   "remaining": {
#     "time": "0:00:02.956173",
#     "absolute": 33,
#     "percentage": 78.57142857142857
#   },
#   "done": {
#     "time": "0:00:00.806229",
#     "absolute": 9,
#     "percentage": 21.428571428571427
#   },
#   "eta": "2021-07-04 18:05:35.103308"
# }
```