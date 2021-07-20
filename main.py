# -*- coding: utf-8 -*-
import os
import random
import sys

import redis

from parameters import *

'''
1. Initialize connection
'''
print("\n***********************************************")
print("********** 1. Initialize Connection. **********")
print("***********************************************\n")
pool = redis.ConnectionPool(host='127.0.0.1', port=6379, decode_responses=True)
r = redis.Redis(host='127.0.0.1', port=6379, decode_responses=True)
r.execute_command('FLUSHALL')

'''
2. Module Load
'''
print("\n***********************************************")
print("*************** 2. Module load. ***************")
print("***********************************************\n")
files = os.listdir('./modules')
for file in files:
    if file.find('.so') != -1:
        file_path = os.path.abspath('.') + '/modules/' + file

        try:
            module_load_ret = r.execute_command('MODULE LOAD', file_path)
        except redis.exceptions.ResponseError:
            print("Module " + file + " load failed, might be loaded already.")
        else:
            print("Module " + file + " load successfully.")

'''
3. Data Generation
'''
print("\n***********************************************")
print("************* 3. Data Generation. *************")
print("***********************************************\n")


# get a random string
def random_str(slen=16, str_type='binary'):
    # type, limit the value range in ascii table
    if str_type == 'binary':
        minval = 0
        maxval = 255
    elif str_type == 'alpha':
        minval = 48
        maxval = 122
    elif str_type == 'compr':
        minval = 48
        maxval = 52

    sa = []
    while slen != 0:
        rr = minval + int(random.random() * (maxval - minval + 1))
        # # avoid putting '\' char in the string, it can mess up TCL processing
        # if str_type == 'alpha' and rr == 92:
        #     rr = 90
        sa.append(chr(rr))
        slen = slen - 1
    return ''.join(sa)


# string-int
for i in range(string_int_num):
    r.set(name=random_str(random.randint(1, 16)),
          value=random.randint(-sys.maxsize - 1, sys.maxsize))

# string-embstr
for i in range(string_emb_num):
    r.set(name=random_str(random.randint(1, 16)),
          value=random_str(random.randint(1, 44)))  # use 39 rather than 44 if redis version <= 3.0

# string-raw
for i in range(string_raw_num - 1):
    r.set(name=random_str(random.randint(1, 16)),
          value=random_str(
              random.randint(44, string_raw_max_field_len - 1)))  # use 39 rather than 44 if redis version <= 3.0

r.set(name='max_field_string_raw', value=random_str(string_raw_max_field_len))

# list-quicklist
for i in range(list_num - 1):
    r.lpush('test-list', random_str(random.randint(1, list_max_field_len - 1)))

r.lpush('test-list', random_str(list_max_field_len))

# set-intset
for i in range(set_intset_num):
    r.sadd('test-set-intset', random.randint(-sys.maxsize - 1, sys.maxsize))

# set-dict
for i in range(set_dict_num - 1):
    r.sadd('test-set-dict', random_str(random.randint(1, set_dict_max_field_len - 1)))

r.sadd('test-set-dict', random_str(set_dict_max_field_len))

# hash-dict
for i in range(hash_dict_num - 1):
    r.hset(name='test-hash-dict',
           key=random_str(random.randint(1, 16)),
           value=random_str(random.randint(1, hash_dict_max_field_len - 1)))

r.hset(name='test-hash-dict',
       key='max_field_hash_dict',
       value=random_str(hash_dict_max_field_len))

# hash-ziplist
for i in range(hash_ziplist_num - 1):
    r.hset(name='test-hash-zl',
           key=random_str(random.randint(1, 16)),
           value=random_str(random.randint(1, hash_ziplist_max_field_len - 1)))

r.hset(name='test-hash-zl',
       key='max_field_hash_ziplist',
       value=random_str(hash_ziplist_max_field_len))

# zset-ziplist
for i in range(zset_ziplist_num - 1):
    r.zadd(name='test-zset-zl',
           mapping={random_str(random.randint(1, zset_ziplist_max_field_len - 1)): random.randint(1, 1000), })

r.zadd(name='test-zset-zl',
       mapping={random_str(random.randint(1, zset_ziplist_max_field_len)): random.randint(1, 1000), })

# zset-skiplist
for i in range(zset_skiplist_num - 1):
    r.zadd(name='test-zset-sl',
           mapping={random_str(random.randint(1, 16)): random.randint(1, 1000), })

r.zadd(name='test-zset-sl',
       mapping={random_str(random.randint(1, zset_skiplist_max_field_len)): random.randint(1, 1000), })

# stream-stream
for i in range(stream_message_num - 1):
    r.xadd(name='test-stream',
           fields={random_str(random.randint(1, 16)): random_str(random.randint(1, 16)), })
r.xadd(name='test-stream', fields={'max_field_stream': random_str(stream_max_field_len), })
'''
4. Get the digest
'''
print(r.execute_command('debug digest'))
r.execute_command('BGSAVE')
