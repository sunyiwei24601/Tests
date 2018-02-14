import redis
import time
pool=redis.ConnectionPool(host='localhost',port=6379)
r=redis.Redis(connection_pool=pool)
r.lpush('list1',11,22,33,44)
print(r.lrange('list1',0,-1))
print(r.llen('list1'))

#指定值的位置插入
r.linsert('list1','after','11','00')
r.lindex('list1',2)


#指定索引号修改
r.lset('list1',5,55)

#移除为55的元素，0代表删除所有，2代表删除从左开始的两个，-2代表从右开始的两个
r.lrem('list1',55,0)

#移除左侧的第一个元素，返回第一个元素，同理有rpop
r.lpop('11')

#删除除了从0开始到5结束的所有其他属性
r.ltrim('list1',0,5)

#从list1右侧pop一个，并转移到list2左侧
r.rpoplpush('list1','list2')

#
