# rdb-generator-python
This is a python script which could generate a customized dump.rdb file by setting parameters.

## 1. Configuration
Install [redis-py](https://github.com/andymccurdy/redis-py), simply:
```bash
pip install redis
```
## 2. Setting Parameter
Edit parameters in `parameters.py`.

You can set the num and length of the data you want

## 3. Module
If you have a self-defined data structure module, you can:
1. run `mkdir modules` to create a folder;
2. put you module.so in the folder;
3. run module commands in `main.py` using `execute_command()`

## 4. Generate dump.rdb
1. start a redis server
2. run `main.py`. Be sure that the host address and the port number matches.
3. get you `dump.rdb`

## 5. Verification
run `debug digest` you can get a data digest value of the db.
This could be used for further verification.
