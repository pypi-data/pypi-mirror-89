import sqlite3


def create_database(path,sql):
    conn = sqlite3.connect(path)
    c = conn.cursor()
    c.execute(sql)
    conn.commit()
    print("成功创建数据库和表")
    conn.close()



def rename_tablename(path,oldname,newname):
    conn = sqlite3.connect(path)
    c = conn.cursor()
    c.execute(f"alter table {oldname} rename to {newname}")
    conn.commit()
    print("成功重命名")
    conn.close()