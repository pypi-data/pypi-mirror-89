import sqlite3
import os


def create_database(path, sql):
    conn = sqlite3.connect(path)
    c = conn.cursor()
    c.execute(sql)
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
