import pymysql

f=open(r'E:\Programing\电子词典\dict.txt')
db=pymysql.connect('localhost','root','123456','dict')
#创建游标
cur=db.cursor()
sql="insert into vocabulary (word,mean) VALUES ('%s','%s')"
for line in f:
    word=line.split('    ')[0]
    mean=line.split('    ')[-1]
    tup=(word,mean)
    try:
     cur.execute(sql,tup)
     db.commit()
    except Exception:
        db.rollback()

f.close()
cur.close()
db.close()
