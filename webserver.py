# encoding=utf-8

import io
import shutil
import urllib.request
import pymysql as mysql_module
import json
from http.server import BaseHTTPRequestHandler, HTTPServer

TABLE = 'user_info'
class MyRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        path, args = urllib.request.splitquery(self.path)  # ?分割
        arg_item = args.split('=')
        user_info = self.getUserInfo(arg_item[1])
        self.output_txt(user_info)

    def getUserInfo(self, args):
        if len(args) != 11 :
            return json.dumps({})
        # 连接数据库
        conn = mysql_module.connect(user='root', passwd='123456',
                 host='localhost', port=3306, db='ring')
        conn.set_charset('utf8')
        cur = conn.cursor()
        select = "select name, sex, company, phone_number, interest, timestamp from " + TABLE + \
                 ' where belong_to = "' + args + '" and inquire = 0'
        cur.execute(select)
        user_info = cur.fetchone()
        if user_info == None :
            cur.close()
            conn.commit()
            conn.close()
            return json.dumps({})
        else :
            update = "update " + TABLE + " SET inquire = 1 where belong_to = " + args + " and timestamp=" + str(user_info[5])
            cur.execute(update)
            cur.close()
            conn.commit()
            conn.close()
            result = {}
            result['name'] = user_info[0]
            result['sex'] = user_info[1]
            result['company'] = user_info[2]
            result ['phone'] = user_info[3]
            result['interest'] = user_info[4]
            return json.dumps(result)

    def do_POST(self):
        path, args = urllib.request.splitquery(self.path)
        length = int(self.headers['content-length'])
        data = self.rfile.read(length)
        self.output_txt(path + args.decode() + data)

    def output_txt(self, content):
        # 指定返回编码
        enc = "UTF-8"
        content = content.encode(enc)
        f = io.BytesIO()
        f.write(content)
        f.seek(0)
        self.send_response(200)
        self.send_header("Content-type", "json; charset=%s" % enc)
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()

        shutil.copyfileobj(f, self.wfile)


PORT = 12138
server = HTTPServer(('', PORT), MyRequestHandler)
print('Started httpServer on port ', PORT)
server.serve_forever()

