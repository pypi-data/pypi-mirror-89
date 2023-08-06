import sqlite3


def create_database(path,sql):
    conn = sqlite3.connect(path)
    c = conn.cursor()
    c.execute(sql)
    conn.commit()
    print("成功创建数据库和表")
    conn.close()

def execute_sqlite(path,sql):
    conn = sqlite3.connect(path)
    c = conn.cursor()
    c.execute(sql)
    conn.commit()
    print("成功执行")
    conn.close()



def rename_tablename(path,oldname,newname):
    conn = sqlite3.connect(path)
    c = conn.cursor()
    c.execute(f"alter table {oldname} rename to {newname}")
    conn.commit()
    print("成功重命名")
    conn.close()




def jointable_withdatabase(inpath,attachpath,tablename):
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


def getinfosbysql(path,field,table):
    conn = sqlite3.connect(path)
    c = conn.cursor()
    c.execute(f"SELECT {field} FROM {table}")
    fetchresult = c.fetchall()
    conn.close()
    result = []
    for i in range(len(fetchresult)):
        result.append(fetchresult[i][0])
    return result