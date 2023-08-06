# -*- coding: utf-8 -*-
from kcweb.config import sqlite as sqliteconfig
import time,traceback,re
import random,sqlite3,os,hashlib
class sqlite:
    __config=sqliteconfig
    __configt={}
    __conn={}
    __cursor={}
    __sql=None
    __sqls=None
    def md5(self,strs):
        """md5加密
        
        参数 strs：要加密的字符串

        return String类型
        """
        m = hashlib.md5()
        b = strs.encode(encoding='utf-8')
        m.update(b)
        return m.hexdigest()
    def close(self):
        "关闭连接"
        for k in sqlite.__conn.keys():
            sqlite.__cursor[k].close()
            sqlite.__conn[k].close()
        sqlite.__conn={}
        sqlite.__cursor={}
        sqlite.__configt={}
    def __setconn(self):
        if not self.__configt:
            self.__configt=sqliteconfig
        try:
            self.__conn[self.md5(self.__configt['db'])]
        except KeyError:
            try:
                if '/' in self.__configt['db']:
                    self.__conn[self.md5(self.__configt['db'])] = sqlite3.connect(self.__configt['db'],check_same_thread=False)
                else:
                    self.__conn[self.md5(self.__configt['db'])] = sqlite3.connect(os.path.split(os.path.realpath(__file__))[0]+"/sqlitedata/"+self.__configt['db'],check_same_thread=False)
            except Exception as e:
                raise Exception(e)
            self.__cursor[self.md5(self.__configt['db'])]=self.__conn[self.md5(self.__configt['db'])].cursor()
    def __execute(self,typess='DQL'):
        self.__setconn()
        # print(self.__sql)
        try:
            res=self.__cursor[self.md5(self.__configt['db'])].execute(self.__sql)
        except Exception as e:
            
            raise Exception(e)
        else:
            return res
    def connect(self,config):
        if isinstance(config,str):
            self.__configt['db']=config
        elif isinstance(config,dict):
            if 'db' in config:
                self.__configt['db']=config['db']
        return self
    __table=""
    def table(self,table):
        """设置表名

        参数 table：str 表名
        """
        self.__table=table
        return self
    def query(self,sql):
        self.__sql=sql
        self.__execute(sql,'DQL')
        # self.close()
    def execute(self,sql):
        self.__sql=sql
        res=self.__execute('DML')
        rowcount=res.rowcount
        # self.close()
        return rowcount
    # def create_table(self):
    #     self.__sql=("CREATE TABLE "+self.__table+
    #     "(ID INT PRIMARY KEY NOT NULL,"+
    #     "NAME TEXT NOT NULL,"+
    #     "AGE INT NOT NULL,"+
    #     "ADDRESS CHAR(50),"+
    #     "SALARY REAL);")
    #     # print(self.__sql)
    #     # exit()
    #     self.execute(self.__sql)
    def select(self,id=None):
        """select查询 

        返回 list(列表)
        """
        if id :
            self.__where="id=%d" % id
        self.__setsql()
        if self.__buildSql:
            self.__sqls="("+self.__sql+")"
            self.__None()
            return self.__sqls
        self.__execute()
        description=self.__cursor[self.md5(self.__configt['db'])].description #获取字段
        result = self.__cursor[self.md5(self.__configt['db'])].fetchall() #获取查询结果
        # self.close()
        lists=[]
        data_dict=[]
        for field in description:#获取字段
            data_dict.append(field[0])
        for k in result:
            i=0
            dicts={}
            for j in k:
                dicts[data_dict[i]]=j
                i=i+1
            lists.append(dicts)
        self.__None(table=False)
        return lists
    def find(self,id=None):
        """查询一条记录
        
        返回 字典
        """
        if id :
            self.__where="id=%s" % id
        self.limit(1)
        self.__setsql()
        if self.__buildSql:
            self.__sqls="("+self.__sql+")"
            self.__None()
            return self.__sqls
      
        self.__execute()
        description=self.__cursor[self.md5(self.__configt['db'])].description #获取字段
        result = self.__cursor[self.md5(self.__configt['db'])].fetchall() #获取查询结果
        # self.close()
        data_dict=[]
        for field in description:#获取字段
            data_dict.append(field[0])
        dicts={}
        for k in result:
            i=0
            for j in k:
                dicts[data_dict[i]]=j
                i=i+1
        self.__None(table=False)
        return dicts
    def count(self,field="*"):
        """查询数量
        
        返回 int 数字
        """
        self.__field=field
        self.__setsql('count')
        if self.__buildSql:
            self.__sqls="("+self.__sql+")"
            return self.__sql
        self.__execute()
        result = self.__cursor[self.md5(self.__configt['db'])].fetchall() #获取查询结果
        # self.close()
        if self.__group:
            cou=len(result)
        else:
            try:
                cou=int(result[0][0])
            except IndexError:
                cou=0
        self.__None(table=False)
        return cou
    def max(self,field):
        """查询某字段的最大值
        
        返回 int 数字
        """
        self.__field=field
        self.__setsql('max')
        if self.__buildSql:
            self.__sqls="("+self.__sql+")"
            return self.__sql
        self.__execute()
        result = self.__cursor[self.md5(self.__configt['db'])].fetchall() #获取查询结果
        # self.close()
        cou=int(result[0][0])
        self.__None(table=False)
        return cou
    def min(self,field):
        """查询某字段的最小值
        
        返回 int 数字
        """
        self.__field=field
        self.__setsql('min')
        if self.__buildSql:
            self.__sqls="("+self.__sql+")"
            return self.__sql
        self.__execute()
        result = self.__cursor[self.md5(self.__configt['db'])].fetchall() #获取查询结果
        # self.close()
        cou=int(result[0][0])
        self.__None(table=False)
        return cou
    def avg(self,field):
        """查询某字段的平均值
        
        返回 int 数字
        """
        self.__field=field
        self.__setsql('avg')
        if self.__buildSql:
            self.__sqls="("+self.__sql+")"
            return self.__sql
        self.__execute()
        result = self.__cursor[self.md5(self.__configt['db'])].fetchall() #获取查询结果
        # self.close()
        cou=int(result[0][0])
        self.__None(table=False)
        return cou
    def sum(self,field):
        """查询某字段之和
        
        返回 int 数字
        """
        self.__field=field
        self.__setsql('sum')
        if self.__buildSql:
            self.__sqls="("+self.__sql+")"
            return self.__sql
        self.__execute()
        result = self.__cursor[self.md5(self.__configt['db'])].fetchall() #获取查询结果
        # self.close()
        cou=int(result[0][0])
        self.__None(table=False)
        return cou
    def update(self,data,affair=False):
        """数据表更新
         
        参数 data 要更新的内容  格式：{"name":"测试","age":20}

        参数 affair 是否开启事务 True表示手动提交事务  False表示自动提交事务
        """
        self.__setsql('update',data)
        res=self.__execute('DML')
        if affair==False and self.__startTrans==False:
            self.commit()
        rowcount=res.rowcount
        # self.close()
        self.__None(table=False)
        return rowcount
    def delete(self,affair=False):
        """数据表删除

        参数 affair 是否开启事务 True表示手动提交事务  False表示自动提交事务
        """
        self.__setsql('delete')
        if self.__where:
            res=self.__execute('DML')
        else:
            return 0
        if affair==False and self.__startTrans==False:
            self.commit()
        rowcount=res.rowcount
        # self.close()
        self.__None(table=False)
        return rowcount
    def insert(self,dicts,affair=False):
        """插入数据库 单条插入或多条插入

        参数 dicts 要插入的内容 单条格式：{"name":"测试","age":20}  。     多条格式：[{"name":"测试","age":20},{"name":"测试","age":20}]
        
        参数 affair 是否开启事务 True表示手动提交事务  False表示自动提交事务

        返回插入的数量
        """
        self.__setsql('insert',dicts)
        res=self.__execute('DML')
        if affair==False and self.__startTrans==False:
            self.commit()
        rowcount=res.rowcount
        # self.close()
        self.__None(table=False)
        return rowcount
    __startTrans=False
    def startTrans(self):
        "开启事务,仅对 update方法、delete方法、install方法有效"
        self.__startTrans=True
    def commit(self):
        """事务提交

        增删改后的任务进行提交
        """
        self.__conn[self.md5(self.__configt['db'])].commit()
    def rollback(self):
        """事务回滚

        增删改后的任务进行撤销
        """
        self.__conn[self.md5(self.__configt['db'])].rollback()
    def getsql(self):
        """得到生成的sql语句"""
        return self.__sql
    __buildSql=None
    def buildSql(self):
        """构造子查询"""
        self.__buildSql=True
        return self
    def __None(self,table=True):
        "清除所有赋值条件"
        self.__lock=None
        self.__distinct=None
        self.__join=None
        self.__joinstr=''
        self.__alias=None
        self.__having=None
        self.__group=None
        self.__group1=None
        self.__order=None
        self.__order1=None
        self.__limit=None
        self.__field="*"
        self.__where=None
        self.__wheres=()
        self.__buildSql=None
        if table:
            self.__table=None
    __where=None
    __wheres=()
    def where(self,where = None,*wheres):
        """设置过滤条件

        传入方式:
        "id",2 表示id='2'

        "id","in",2,3,4,5,6,...表示 id in (2,3,4,5,6,...)

        "id","in",[2,3,4,5,6,...]表示 id in (2,3,4,5,6,...)

        [("id","gt",6000),"and",("name","like","%超")] 表示 ( id > "6000" and name LIKE "%超" )

        "id","eq",1 表示 id = '1'

        eq 等于
            neq 不等于
            gt 大于
            egt 大于等于
            lt 小于
            elt 小于等于
            like LIKE
        """
        self.__where=where
        self.__wheres=wheres
        # print(len(self.__wheres))
        return self
    __field='*'
    def field(self,field = "*"):
        """设置过滤显示条件

        参数 field：str 字符串
        """
        self.__field=field
        return self
    __limit=[]
    def limit(self,offset, length = None):
        """设置查询数量

        参数 offset：int 起始位置

        参数 length：int 查询数量
        """
        self.__limit=[offset,length]
        return self
    def page(self,pagenow=1, length = 20):
        """设置分页查询

        参数 pagenow：int 页码

        参数 length：int 查询数量
        """
        offset=(pagenow-1)*length
        self.__limit=[offset,length]
        return self
    __order=None
    __order1=None
    def order(self,strs=None,*strs1):
        """设置排序查询

        传入方式:

        "id desc"

        "id",'name','appkey','asc'

        "id",'name','appkey'   不包含asc或desc的情况下 默认是desc

        ['id','taskid',{"task_id":"desc"}]
        """
        self.__order=strs
        self.__order1=strs1
        return self
    __group=None
    __group1=None
    def group(self,strs=None,*strs1):
        """设置分组查询

        传入方式:

        "id,name"

        "id","name"
        """
        self.__group=strs
        self.__group1=strs1
        return self
    __having=None
    def having(self,strs=None):
        """用于配合group方法完成从分组的结果中筛选（通常是聚合条件）数据

        参数 strs：string 如："count(time)>3"
        """
        self.__having=strs
        return self
    
    __alias=None
    def alias(self,strs=None):
        """用于设置当前数据表的别名，便于使用其他的连贯操作例如join方法等。

        参数 strs：string 默认当前表作为别名
        """
        if strs:
            self.__alias=strs
        else:
            self.__alias=self.__table
        return self
    __join=None
    __joinstr=''
    def join(self,strs,on=None,types='INNER'):
        """用于根据两个或多个表中的列之间的关系，从这些表中查询数据

        参数 strs  string 如："test t1"   test表设置别名t1

        参数 on  string 如："t1.id=t2.pid"   设置连接条件

        参数 types  支持INNER、LEFT、RIGHT、FULL  默认INNER

        """
        joinstr=''
        if strs and on:
            joinstr=joinstr+types+" JOIN "+strs+" ON "+on+" "
        if joinstr:
            self.__joinstr=self.__joinstr+joinstr
        return self
    __distinct=None
    def distinct(self,bools=None):
        "用于返回唯一不同的值,配合field方法使用生效,消除所有重复的记录，并只获取唯一一次记录。"
        self.__distinct=bools
        return self
    __lock=None
    def lock(self,strs=None):
        """用于数据库的锁机制，在查询或者执行操作的时候使用  （暂未实现）

        排他锁 (Exclusive lock)

        共享锁 (Shared lock)
        
        参数 strs  如：True表示自动在生成的SQL语句最后加上FOR UPDATE，

        
        """
        # self.__lock=strs
        return self
    def __setsql(self,types=None,data = {}):
        """生成sql语句"""
        if types==None:
            self.__sql="SELECT"
            if self.__distinct and self.__field:
                self.__sql=self.__sql+" DISTINCT"
            if self.__alias:
                self.__sql=self.__sql+" %s FROM %s %s" % (self.__field,self.__table,self.__alias)
            else:
                self.__sql=self.__sql+" %s FROM %s" % (self.__field,self.__table)
        elif types=='count':
            self.__sql="SELECT COUNT(%s) FROM %s" % (self.__field,self.__table)
        elif types=='max':
            self.__sql="SELECT MAX(%s) FROM %s" % (self.__field,self.__table)
        elif types=='min':
            self.__sql="SELECT MIN(%s) FROM %s" % (self.__field,self.__table)
        elif types=='avg':
            self.__sql="SELECT AVG(%s) FROM %s" % (self.__field,self.__table)
        elif types=='sum':
            self.__sql="SELECT SUM(%s) FROM %s" % (self.__field,self.__table)
        elif types=='update':
            strs=''
            for k in data:
                if isinstance(data[k],str):
                    strs=strs+" %s = '%s' ," % (k,self.escape_string(data[k]))
                else:
                    strs=strs+" %s = %s ," % (k,data[k])
            strs=strs[:-1]
            self.__sql="UPDATE %s SET %s" % (self.__table,strs)
            # print(self.__sql)
        elif types=='delete':
            self.__sql="DELETE FROM %s" % (self.__table)
        elif types=='insert':
            if isinstance(data,dict):
                strs=''
                val=''
                for k in data:
                    strs=strs+"%s," % k
                    if isinstance(data[k],str):
                        val=val+"'%s'," % self.escape_string(data[k])
                    else:
                        val=val+"%s," % data[k]
                strs=strs[:-1]
                val=val[:-1]
                self.__sql="INSERT INTO "+str(self.__table)+" ("+strs+") VALUES ("+val+")"
                # print(self.__sql)
            elif isinstance(data,list):
                strs=''
                val='('
                for k in data[0]:
                    strs=strs+" , "+k
                for k in data:
                    for j in k:
                        if isinstance(k[j],str):
                            val=val+"'"+str(k[j])+"',"
                        else:
                            val=val+str(k[j])+","
                    val=val[:-1]
                    val=val+"),("
                val=val[:-2]
                self.__sql="INSERT INTO "+str(self.__table)+" ("+strs[3:]+") VALUES "+val
        
        if self.__joinstr:
            # print(self.__sql)
            self.__sql=self.__sql+" "+self.__joinstr
        if self.__where:
            if isinstance(self.__where,str):
                if self.__wheres:
                    if len(self.__wheres) == 2:
                        if isinstance(self.__wheres[1],list):
                            self.__sql=self.__sql + " WHERE %s %s (" % (self.__where,self.__operator(self.__wheres[0]))
                            for k in self.__wheres[1]:
                                self.__sql=self.__sql+str(k)+","
                            self.__sql=self.__sql[:-1]+")"
                        else:
                            self.__sql=self.__sql + " WHERE  %s %s '%s'" % (self.__where,self.__operator(self.__wheres[0]),self.__wheres[1])
                    elif len(self.__wheres) > 2:
                        if self.__wheres[0]=='in':
                            strs=str(self.__wheres[1])
                            i=0
                            for k in self.__wheres:
                                if i > 1:
                                    strs=strs+","+str(k)
                                i=i+1
                            self.__sql=self.__sql + " WHERE  %s in (%s)" % (self.__where,strs)
                    else:
                        self.__sql=self.__sql + " WHERE  %s = '%s'" % (self.__where,self.__wheres[0])
                else:
                    self.__sql=self.__sql + " WHERE  %s" % self.__where
            elif isinstance(self.__where,list):
                self.__sql=self.__sql + " WHERE  %s" % self.__listTrans()
            else:
                print("参数where类型错误",type(self.__where),self.__where)
        if self.__order:
            s=''
            if isinstance(self.__order,list):
                for strs in self.__order:
                    if isinstance(strs,str):
                        s=s+strs+","
                    else:
                        pass
                        for key in strs:
                            s=s+key+" "+strs[key]
                        s=s+","
                s=s[:-1]
            if isinstance(self.__order,str):
                if self.__order1:
                    if len(self.__order1) > 1:
                        if self.__order1[len(self.__order1)-1] == 'desc' or self.__order1[len(self.__order1)-1] == 'asc':
                            i=0
                            while i<len(self.__order1)-1:
                                s=s+self.__order1[i]+","
                                i=i+1
                            s=s[:-1]+" "+self.__order1[len(self.__order1)-1]
                        else:
                            for key in self.__order1:
                                s=s+key+","
                            s=s[:-1]
                            s=s+" asc"
                        s=self.__order+","+s
                    else:
                        s=s[:-1]+self.__order1[0]
                        s=self.__order+" "+s
                else:
                    s=self.__order
                # print(s)
            self.__sql=self.__sql+" ORDER BY "+s
        if self.__group:
            s=self.__group
            if self.__group1:
                for key in self.__group1:
                    s=s+","+key
            self.__sql=self.__sql+" GROUP BY "+s
        if self.__having:
            self.__sql=self.__sql+" HAVING "+self.__having
        if self.__limit:
            if self.__limit[1]:
                self.__sql=self.__sql+" LIMIT %d,%d" % (self.__limit[0],self.__limit[1])
            else:
                self.__sql=self.__sql+" LIMIT %d" % self.__limit[0]
        if self.__lock:
            if isinstance(self.__lock,str):
                self.__sql=self.__sql+" "+self.__lock
            else:
                self.__sql=self.__sql+' Exclusive lock'
        # print(self.__sql)
    def __listTrans(self):
        """列表转换sql表达式
        返回 字符串
        """
        strs=''
        #[('id', 'eq', '1'), 'or', ('id', 'eq', '2')]
        for k in self.__where:
            if isinstance(k,tuple):
                t=0
                for j in k:
                    if t==0:
                        strs=strs+' '+str(j)+' '
                    elif t==1:
                        strs=strs+self.__operator(j)
                    if t==2:
                        strs=strs+' "'+str(j)+'" '
                    t=t+1
            elif isinstance(k,str):
                strs=strs+k
        return "("+strs+")"
    def __operator(self,strs):
        """运算符转换
        参数 strs 待转的字符串
        返回 已转换的运算符

        符号定义
            eq 等于
            neq 不等于
            gt 大于
            egt 大于等于
            lt 小于
            elt 小于等于
            like LIKE
        """
        strss=strs.upper()
        if strss == 'EQ':
            k='='
        elif strss == 'NEQ':
            k='<>'
        elif strss == 'GT':
            k='>'
        elif strss == 'EGT':
            k='>='
        elif strss == 'LT':
            k='<'
        elif strss == 'ELT':
            k='<='
        elif strss == 'LIKE':
            k='LIKE'
        else:
            k=strss
        return k
    def escape_string(self,value):
        """sqlite3 字符串转义

        Value 字符串
        """
        # value = value.replace('/', '//')
        value = value.replace("'", "''")
        # value = value.replace('[', '/[')
        # value = value.replace(']', '/]')
        # value = value.replace('%', '/%')
        # value = value.replace('&', '/&')
        # value = value.replace('_', '/_')
        # value = value.replace('(', '/(')
        # value = value.replace(')', '/)')
        return value

    
    