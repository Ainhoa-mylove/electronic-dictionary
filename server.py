"""
dict服务端部分
处理请求逻辑
"""
from socket import *
from opreation_db import *
import sys
from threading import Thread

#全局变量
PORT=8888
HOST='127.0.0.1'
ADDR=(HOST,PORT)
#注册
def do_register(c,db,data):
    tmp=data.split(' ')
    name=tmp[1]
    passwd=tmp[2]

    if db.register(name,passwd):
        c.send(b'OK')
    else:
        c.send(b'False')
#登录
def do_login(c,db,data):
    tmp=data.split(' ')
    name=tmp[1]
    passwd=tmp[2]
    if db.login(name,passwd):
        c.send(b'OK')
    else:
        c.send(b'False')
#查询
def do_query(c,db,data):
    tmp = data.split(' ')
    name = tmp[1]
    word = tmp[2]
    #插入历史记录
    db.insert_history(name,word)
    #查单词
    mean=db.do_query(word)
    if not mean:
        c.send('没有找到该单词'.encode())
    else:
        msg='%s : %s'%(word,mean)
        c.send(msg.encode())

#处理客户端请求
def do_request(c,db):
    db.create_cursor()#生成游标 db.cur
    while True:
        data=c.recv(1024).decode()
        print(c.getpeername(),':',data)
        if not data or data[0] == 'E':
            c.close()
            sys.exit('客户端退出')
        elif data[0]=='R':
            do_register(c,db,data)
        elif data[0]=='L':
            do_login(c,db,data)
        elif data[0]=='Q':
            do_query(c,db,data)

# 网络连接
def main():
    #创建数据库连接对象
    db=Database()
    #创建TCP套接字
    s=socket()
    #端口重用
    s.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
    s.bind(ADDR)
    s.listen(5)

    #处理僵尸进程,只能在lunix下运行
    # signal.signal(signal.SIGCHLD,signal.SIG_IGN)

    #等待客户端的链接
    print('Listen the port 8888')
    while True:
        try:
            c,addr=s.accept()
            print('Connect from:',addr)
        except KeyboardInterrupt:
            s.close()
            sys.exit('服务器退出!!!')
        except Exception as e:
            print(e)
            continue
        #创建子进程
        p=Thread(target=do_request,args=(c,db))
        p.daemon=True
        p.start()

if __name__ == '__main__':
    main()
