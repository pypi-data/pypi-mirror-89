#coding:utf-8
from flask import Flask,request,render_template

import time
import copy

app = Flask(__name__, static_url_path='')

userlog=['张三','李四','王五']

@app.route('/uestc/<user>/',methods=['get'])
def uestc(user):
    userlog.append(user+' '+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+" 出校")
    return render_template('index.html',user=user)

@app.route('/uestc2/<user>/',methods=['get'])
def uestc2(user):
    userlog.append(user+' '+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+" 入校")
    return render_template('index2.html',user=user)

@app.route('/log/<pwd>/',methods=['get'])
def log(pwd):
    if pwd=="mrlution":
        templist= copy.deepcopy(userlog)
        templist.reverse()
        temp=''
        for item in templist:
            temp=temp+item+'<br>'
        return temp
    else:
        return "who are you?"




if __name__ == '__main__':
    app.run(host='0.0.0.0',
    port= 5000,
    debug=True)

