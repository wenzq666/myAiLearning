import redis

r = redis.Redis(host='192.168.88.128',decode_responses=True)

r.set('name','迪丽热巴')
r.set('name','古力娜扎')
a = r.get('name')

print(a)

r.mset(mapping={'age':18,'gender':'🚺'})

m = r.mget(keys=['name','age','gender'])
print(m)


r.set('amount',0)
r.incr('amount')
r.incrby('amount',amount=15)

print(r.get('amount'))


r.close()























