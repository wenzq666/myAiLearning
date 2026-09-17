import redis

r = redis.Redis(host='192.168.88.128',decode_responses=True)


r.hset('stu:1001','name','迪丽热巴')
r.hset('stu:1001','age',18)
r.hset('stu:1001','gender','🚺')

print(r.hget('stu:1001', 'gender'))

print(r.hgetall('stu:1001'))
print(r.hgetall('stu:1002'))

r.hset('stu:1002','name','古力娜扎')
r.hset('stu:1002','age',18)
r.hset('stu:1002','gender','🚺')

r.hset('stu:1003','name','马儿扎哈')
r.hset('stu:1003','age',18)
r.hset('stu:1003','gender','🚺')
print(r.hgetall('stu:1003'))

r.delete('stu:1003')

r.close()























