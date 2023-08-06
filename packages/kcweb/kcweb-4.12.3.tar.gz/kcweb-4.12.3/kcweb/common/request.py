# -*- coding: utf-8 -*-
from kcweb.common import globals as kcwglobals
import json,urllib
class args:
    "获取url"
    def params():
        return urllib.parse.parse_qs(urllib.parse.urlparse(kcwglobals.HEADER.URL).query)
    def get(name):
        """获取键值对
        
        name 键

        return 值
        """
        params = args.params()
        try:
            k=params[name][0]
        except:
            k=''
        return k
    def get_json():
        """获取 json get内容

        return  json内容
        """
        try:
            lists=kcwglobals.HEADER.URL.split("?")[1]
            lists=lists.split("&")
            data={}
            for k in lists:
                ar=k.split("=")
                data[ar[0]]=ar[1]
            return data
        except:return None
class froms:
    "获取from  application/x-www-form-urlencoded 的post内容"
    def get(name):
        """获取键值对
        
        name 键

        return 值
        """
        data=kcwglobals.HEADER.BODY_DATA
        params = urllib.parse.parse_qs(urllib.parse.urlparse("?"+str(data)).query)
        try:
            k=urllib.parse.unquote(params[name][0])
        except:
            k=None
        return k
    def get_json():
        """获取post json post内容

        return  json内容
        """
        try:
            lists=kcwglobals.HEADER.BODY_DATA.split("&")
            data={}
            for k in lists:
                ar=k.split("=")
                data[ar[0]]=urllib.parse.unquote(ar[1])
            return data
        except:return None
class binary:
    "二进制或文件处理"
    def get(name):
        """获取文件二进制

        name 文件标识

        return 文件二进制
        """
        return kcwglobals.HEADER.files[name].value
    def filename(name):
        """获取文件名，上传文件时有效，其他情况返回空

        name 文件标识

        return 文件名
        """
        return kcwglobals.HEADER.files[name].filename
    def filesuffix(name):
        """获取文件后缀，上传文件时有效，其他情况返回空

        name 文件标识

        return 文件名
        """
        return kcwglobals.HEADER.files[name].filename.split('.')[-1]
    def save(name,filename):
        """保存二进制文件
        
        name 文件标识

        filename 文件位置

        return 完整文件名
        """
        if kcwglobals.HEADER.files[name].value:
            open(filename, 'wb').write(kcwglobals.HEADER.files[name].value)
            return filename
        else:
            return None
class HEADER:
    def GET():
        return kcwglobals.HEADER.GET
    def Method():
        return kcwglobals.HEADER.Method
    def URL():
        return kcwglobals.HEADER.URL.lstrip()
    def PATH_INFO():
        return kcwglobals.HEADER.PATH_INFO.lstrip()
    def SERVER_PROTOCOL():
        return kcwglobals.HEADER.SERVER_PROTOCOL
    def HTTP_HOST():
        return kcwglobals.HEADER.HTTP_HOST
    def HTTP_COOKIE():
        return kcwglobals.HEADER.HTTP_COOKIE
    def HTTP_USER_AGENT():
        return kcwglobals.HEADER.HTTP_USER_AGENT
    def REMOTE_ADDR():
        return kcwglobals.HEADER.REMOTE_ADDR
    def HTTP_X_REAL_IP():
        "nginx服务器发送的客户端IP"
        return kcwglobals.HEADER.HTTP_X_REAL_IP
    def Physical_IP():
        "获取访问用户物理ip"
        if kcwglobals.HEADER.HTTP_X_REAL_IP:
            return kcwglobals.HEADER.HTTP_X_REAL_IP
        else:
            return kcwglobals.HEADER.REMOTE_ADDR
    # def url_scheme():
    #     "获取http类型  待测试"
    #     return kcwglobals.HEADER.url_scheme
def get_data():
    "获取请求参数体"
    return kcwglobals.HEADER.BODY_DATA
def get_json():
    "获取请求参数体json"
    try:
        return json.loads(kcwglobals.HEADER.BODY_DATA)
    except:
        return None
def getroutecomponent():
    "获取路由"
    return kcwglobals.VAR.component
