from datetime import datetime
import time
a=datetime.now()
time.sleep(1)
b=datetime.now()
print(a)
print(b)
print((b-a).days)