# -*- coding:utf-8 -*-  
__author__ = 'hklliang'
__date__ = '2017-08-29 13:45'
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column,Integer,String
engine = create_engine("mysql+pymysql://root:root@localhost/testdb?charset=utf8",
                       encoding='utf-8')# echo=True显示调试信息
Session_class = sessionmaker(bind=engine)  # 创建与数据库的会话session class ,注意,这里返回给session的是个class,不是实例
Session = Session_class()  # 生成session实例,相当于cursor
Base = declarative_base()
class Host(Base):
    __tablename__='host'
    id=Column(Integer,primary_key=True)
    hostname=Column(String(64),unique=True)
    ip=Column(String(64),unique=True)
    port=Column(Integer,default=22)

    def __repr__(self):
        return self.hostname



class HostGroup(Base):
    __tablename__='host_group'
    name=Column(String(64),unique=True)

    def __repr__(self):
        return self.name


class RemoteUser(Base):
    __tablename__='host_group'
    name=Column(String(64),unique=True)

    def __repr__(self):
        return self.name