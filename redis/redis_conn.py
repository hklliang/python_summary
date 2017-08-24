import redis
pool=redis.ConnectionPool()
r=redis.Redis(connection_pool=pool)
r.set('foo','Bar')
print(r.get('foo'))