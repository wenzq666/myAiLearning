import redis

r = redis.Redis(host='192.168.88.128',decode_responses=True)

# 从左添加元素
r.lpush('tasks','t1','t2','t3')

# 从右添加元素
r.rpush('tasks','t44','t55','t66')

print(r.lrange('tasks', 0, -1))

lp = r.lpop(name='tasks',count=3)
print(lp)

print(r.lrange('tasks', 0, -1))

print('*'*20)
rp = r.rpop(name='tasks',count=2)
print(rp)
print(r.lrange('tasks', 0, -1))

r.flushdb()
r.close()























