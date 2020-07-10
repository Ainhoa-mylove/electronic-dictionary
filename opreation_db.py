"""
dict用于处理数据

"""
import pymysql
import hashlib
import time

#编写功能类提供给服务端使用
class Database:
    def __init__(self,host='localhost',port=3306,
                 user='root',passwd='123456',
                 database='dict',charset='utf8'):
        self.host=host
        self.port=port
        self.user=user
        self.passwd=passwd
        self.database=database
        self.charset=charset
        self.connect_db()

        #链接数据库
    def connect_db(self):
        self.db=pymysql.connect(host=self.host,
                                port=self.port,
                                user=self.user,
                                passwd=self.passwd,
                                database=self.database,
                                charset=self.charset)
        #注册
    def register(self,name,passwd):
        sql="select * from user where name='%s'"%name
        self.cur.execute(sql)
        r=self.cur.fetchone()
        if r:
            return False
        #加密处理
        hash=hashlib.md5((name+"AKA868").encode())
        hash.update(passwd.encode())
        sql="insert into user (name,passwd) values (%s,%s)"
        try:
            self.cur.execute(sql,[name,hash.hexdigest()])
            self.db.commit()
            return True
        except Exception:
            return False
        #登录
    def login(self,name,passwd):
        sql = "select * from user where name='%s' and passwd='%s'"
        hash=hashlib.md5((name+"AKA868").encode())
        hash.update(passwd.encode())
        sql=sql%(name,hash.hexdigest())
        self.cur.execute(sql)
        r = self.cur.fetchone()
        if r:
            return True
        else:
            return False
        #插入历史记录
    def insert_history(self,name,word):
        tm=time.ctime()
        sql="insert into history_record (name,word,time) values (%s %s %s)"
        try:
            self.cur.execute(sql,[name,word,tm])
        except Exception:
            self.db.rollback()

        #查询单词
    def do_query(self,word):
        sql="select mean from vocabulary where word = '%s'"%word
        self.cur.execute(sql)
        r=self.cur.fetchone()
        if r:
            return r[0]

    def create_cursor(self):
        self.cur=self.db.cursor()
    def close(self):
        self.cur.close()
        self.db.close()
