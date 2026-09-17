import redis

r = redis.Redis(host='192.168.88.128',decode_responses=True)

# 添加有序集合
r.zadd('zset1',mapping={'p1':1000,'p2':3000,'p3':2000})

# 升序
print(r.zrange('zset1',start=0,end=-1,withscores=True))

# 降序
print(r.zrevrange('zset1', start=0, end=-1, withscores=True))

print(r.zscore('zset1', 'p2'))

print(r.zincrby('zset1', '100', 'p1'))


print(r.zrange('zset1',start=0,end=-1,withscores=True))
# 获取升序排名元素  从0开始
print(r.zrank(name='zset1', value='p1'))

print(r.zrangebyscore(name='zset1', min=2000, max=3000, withscores=True))

#r.flushdb()
r.close()























