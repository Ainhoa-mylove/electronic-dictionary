"""
dict客户端
发起请求，展示结果
"""
from socket import *
import hashlib
import sys

PORT = 8888
HOST = '127.0.0.1'
ADDR = (HOST,PORT)
#所有函数都用S
s = socket()
s.connect(ADDR)
#一级界面注册
def do_register():
    while True:
        name=input('User:')
        passwd=input('Password')
        passwd1=input('Again:')

        if (' 'in name)or(' 'in passwd):
            print('用户名与密码不能有空格！！')
            continue
        if passwd!=passwd1:
            print('两次密码不一致！！')
            continue

        msg='R %s %s'%(name,passwd)
        #发送请求
        s.send(msg.encode())
        data=s.recv(128).decode()
        if data=='OK':
            print('注册成功！')
            second_page(name)
        else:
            print('注册失败！')
        return

#一级界面登录
def do_login():
    name = input('User:')
    passwd = input('Password:')
    msg="L %s %s"%(name,passwd)
    s.send(msg.encode())
    #等待反馈
    data = s.recv(128).decode()
    if data == 'OK':
        print('登录成功！')
        second_page(name)
    else:
        print('登录失败！')
    return

#二级界面查单词
def do_query(name):
    while True:
        word=input('请输入想要查询的单词：')
        #结束查询单词
        if word=='##':
            break
        msg='Q %s %s'%(name,word)
        s.send(msg.encode())
        #等待回复
        data=s.recv(2048).decode()
        print(data)

#二级界面
def second_page(name):
    while True:
        print("""
                ====================Query==================
                1、查单词         2、历史记录          3、注销
                ===========================================
                """)
        cmd = input('输入选项：')
        if cmd == '1':
            do_query(name)
        elif cmd == '2':
            pass
        elif cmd == '3':
            return
        else:
            print('请输入正确命令！！！！')
def main():
    while True:
        print("""
        ===============Welcome===============
        1、注册         2、登录          3、退出
        =====================================
        """)
        cmd=input('输入选项：')
        if cmd=='1':
            do_register()
        elif cmd=='2':
            do_login()
        elif cmd=='3':
            s.send(b'E')
            print('谢谢使用！')
            return
        else:
            print('请输入正确命令！！！！')


if __name__ == '__main__':
    main()
