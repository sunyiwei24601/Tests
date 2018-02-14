import redis
import time
r=redis.Redis(host='localhost',port=6379)
pipe=r.pipeline(transaction=True)
r.set('name','carl')
r.set('time',time.ctime())
r.mset({'first':'Sun','last':'YiWei'})
print(r.mget('first','last'))
pipe.execute()