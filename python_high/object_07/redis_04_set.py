import redis

r = redis.Redis(host='192.168.88.128',decode_responses=True)

# 添加集合
r.sadd('s1','11','22','33','44')

# 随机删
#r.spop('s1',count=2)

# 指定删除
r.srem('s1','33')

print(r.smembers('s1'))

r.sadd('s2','11','22','33','44')
r.sadd('s3','11','22','33','55')

print(r.sinter(['s2', 's3']))
print(r.sunion(['s2', 's3']))
print(r.sdiff(['s2', 's3']))
print(r.sdiff(['s3', 's2']))



#r.flushdb()
r.close()























