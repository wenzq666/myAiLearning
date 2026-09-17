import time

import redis

r = redis.Redis(host='192.168.88.128',decode_responses=True)

r.set('session:user1001','admin')

print(r.get('session:user1001'))


r.expire('session:user1001',15)
time.sleep(4)

print(r.ttl('session:user1001'))

#r.flushdb()
r.close()























