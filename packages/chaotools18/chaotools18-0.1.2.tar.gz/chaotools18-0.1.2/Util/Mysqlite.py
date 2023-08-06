import sqlite3
import os


def create_database(path, sql):
    conn = sqlite3.connect(path)
    c = conn.cursor()
    c.execute(sql)
    conn.commit()
    conn.close()
    print("成功创建数据库和表")


def create_tables(path, *args):
    conn = sqlite3.connect(path)
    c = conn.cursor()
    for arg in args:
        c.execute(arg)
        conn.commit()
    conn.close()
    print("成功创建数据库和表")


def execute_sqlite(path, sql):
    conn = sqlite3.connect(path)
    c = conn.cursor()
    c.execute(sql)
    conn.commit()
    conn.close()
    print("成功执行")


def rename_tablename(path, oldname, newname):
    if not os.path.exists(path):
        raise FileNotFoundError("文件不存在")
    conn = sqlite3.connect(path)
    c = conn.cursor()
    c.execute(f"alter table {oldname} rename to {newname}")
    conn.commit()
    conn.close()
    print("成功重命名")


def jointable_withdatabase(inpath, attachpath, tablename):
    if not os.path.exists(inpath) or not os.path.exists(attachpath):
        raise FileNotFoundError("文件不存在")
    conn = sqlite3.connect(inpath)
    conn.text_factory = str
    cur = conn.cursor()
    attach = 'attach database "' + attachpath + '" as temp_db;'
    sql1 = f'insert into {tablename} select * from temp_db.{tablename};'
    cur.execute(attach)
    cur.execute(sql1)
    conn.commit()
    conn.close()
    print("成功")

def jointables_withdatabases(inpath,attachpaths,tablename):
    for item in attachpaths:
        if not os.path.exists(item):
            raise FileNotFoundError("文件不存在")
    if not os.path.exists(inpath):
        raise FileNotFoundError("文件不存在")


    conn = sqlite3.connect(inpath)
    conn.text_factory = str
    cur = conn.cursor()
    for attachpath in attachpaths:
        attach = 'attach database "' + attachpath + '" as temp_db;'
        sql1 = f'insert or ignore into {tablename} select * from temp_db.{tablename};'
        cur.execute(attach)
        cur.execute(sql1)
        conn.commit()
    conn.close()
    print("成功")




def getinfosbysql(path, field, table):
    if not os.path.exists(path):
        raise FileNotFoundError("文件不存在")
    conn = sqlite3.connect(path)
    c = conn.cursor()
    c.execute(f"SELECT {field} FROM {table}")
    fetchers = c.fetchall()
    conn.close()
    result = []
    for i in range(len(fetchers)):
        result.append(fetchers[i][0])
    return result


def select_info_by_dict(path,indict,table):
    conn = sqlite3.connect(path)
    c = conn.cursor()
    c.execute(f"SELECT * FROM {table}")
    fetchers = c.fetchall()
    conn.close()
    result = []
    for i in range(len(fetchers)):
        keys = [key for key in indict.keys()]
        detailinfo={}
        for j in range(len(keys)):
            key = keys[j]
            detailinfo[key] = fetchers[i][j]
        result.append(detailinfo)
    return result


