#!/usr/bin/env python
#coding=utf-8
#功能 ：封装企业微信群机器人API
#日期 ：2021-09-05 
#作者：Dark-Athena
#EMAIL:darkathena@qq.com
#说明：
""" 
 支持纯文本、markdown、图片、文件、图文
 a = wx.WxRobot('1111-222-333-444-55555') #webhook
 a.sendMessage('文本内容')
 a.sendMarkdown('markdown内容')
 a.sendImage('d:/图片.jpg') #图片文件的绝对路径
 a.sendMedia('d:/文件.jpg') #文件的绝对路径

 a.sendNews('[{
               "title" : "中秋节礼品领取",
               "description" : "今年中秋节公司有豪礼相送",
               "url" : "www.qq.com",
               "picurl" : "http://res.mail.qq.com/node/ww/wwopenmng/images/independent/doc/test_pic_msg1.png"
           }]')
"""
           
import requests
import json
import hashlib
import base64
import os

class WxRobot():
    headers = {"Content-Type": "application/json"}
    req_message = {"errcode": 1,"errmessage": "请求微信企业失败，请检查网络"}
    
    def __init__(self, webhook):
        self.post_url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={0}".format(webhook)
        
    def _req(self,data):
        try:
            return requests.post(self.post_url, data=json.dumps(data), headers=self.headers,timeout=10).json()
        except Exception as e:
            return self.req_message
            
    def sendMessage(self, message):
        data = {"msgtype": "text","text": {"content": str(message)}}
        return self._req(data)
    
    def sendMarkdown(self, message):
        data = {"msgtype": "markdown","markdown": {"content": str(message)}}
        return self._req(data)
        
    def sendNews(self, message):
        data = {"msgtype": "news","news": {"articles": list(message)}}
        print (data)
        return self._req(data)  
                 
    def sendImage(self, image_path):
        if os.path.exists(image_path):
            with open(image_path, "br") as f:
                fcont = f.read()
                ls_f = base64.b64encode(fcont)
                fmd5 = hashlib.md5(fcont)
                data = {"msgtype": "image", "image": {"base64": ls_f.decode('utf8'), "md5": fmd5.hexdigest()}}
                return self._req(data) 
        else:
            self.req_message['errmessage']='图片文件不存在'
            return self.req_message
            
    def sendMedia(self, file_path):
        if os.path.exists(file_path):
            upload_url = self.post_url.replace('send', 'upload_media') + '&type=file'
            try:
                media_id = requests.post(upload_url, files=[('media', open(file_path, 'rb'))]).json()['media_id'] 
                print (media_id)
            except Exception as e:
                self.req_message['errmessage']='上传文件失败，请检查网络'
                return self.req_message   
            data = {"msgtype": "file","file": {"media_id": media_id}}
            return self._req(data)
        else:
            self.req_message['errmessage']='文件不存在'
            return self.req_message
        
