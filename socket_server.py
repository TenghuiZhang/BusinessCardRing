#-*- coding:utf-8 -*-

from socketserver import (TCPServer as TCP, StreamRequestHandler  as SRH, ThreadingMixIn as TMI)
import traceback
import pymysql as mysql_module


TABLE = 'user_info'
earlyData = ''

class MyBaseRequestHandler(SRH):

    """
    #从BaseRequestHandler继承，并重写handle方法
    """
    def handle(self):
        try:
            global earlyData
            #一次读取1024字节,并去除两端的空白字符(包括空格,TAB,\r,\n)
            data = self.request.recv(1024).strip().decode('gbk')
            #self.client_address是客户端的连接(host, port)的元组
            print("receive from (%r):%s" % (self.client_address, data))
            if earlyData == '':
                earlyData = data
            else:
                # 解析新接收数据的时间，时间相差1s储存
                if self.isValidInternal(data) :
                    # 将两条数据存入数据库为http请求做准备
                    self.saveToSql(data)
                    earlyData = ''
                else :
                    earlyData = data
                
            #转换成大写后写回(发生到)客户端
            # self.request.sendall(data.upper())
        except:
            traceback.print_exc()
            # break
        #循环监听（读取）来自客户端的数据
        #while True:


    def isValidInternal(self, data):
        return abs(float(data.split(' ')[0]) - float(earlyData.split(' ')[0])) <= 1.5

    insertData = 'insert into ' + TABLE + ' (belong_to, timestamp, name, sex, company, phone_number, interest) ' \
                                    'values(%s, %s, %s, %s, %s, %s, %s)'
    def saveToSql(self, data):
        global earlyData
    
		
        # 连接数据库
        conn = mysql_module.connect(user='root', passwd='123456',
                 host='localhost', port=3306, db='ring')
        conn.set_charset('utf8')
        cur = conn.cursor()
        items1 = data.split(' ')
        items1.insert(0, earlyData.split(' ')[4])
        items2 = earlyData.split(' ')
        items2.insert(0, data.split(' ')[4])
        cur.executemany(self.insertData,
                        [tuple(items1),
                        tuple(items2)])
        #sql="select * from " + TABLE
        #print(execute(sql))
        #print(cur.fetchone())
        cur.close()
        conn.commit()
        print("存入数据库成功")
        conn.close()

PORT = 9999     #端口
ADDR = ('', PORT)

class Server(TMI, TCP):                                         #变动位置
    pass

if __name__ == "__main__":
    # 初始化TCPServer对象，
    server = Server(ADDR, MyBaseRequestHandler)
    # 启动服务监听
    server.serve_forever()
