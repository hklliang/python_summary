
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String,ForeignKey
from sqlalchemy.orm import sessionmaker,relationship

engine = create_engine("mysql+pymysql://root:root@localhost/testdb?charset=utf8",
                       encoding='utf-8')# echo=True显示调试信息
Session_class = sessionmaker(bind=engine)  # 创建与数据库的会话session class ,注意,这里返回给session的是个class,不是实例
Session = Session_class()  # 生成session实例,相当于cursor
Base = declarative_base()  # 生成orm基类


class User(Base):
    __tablename__ = 'user'  # 表名
    id = Column(Integer, primary_key=True)
    name = Column(String(32))
    password = Column(String(255))


    def __repr__(self):
        return '%s,%s'%(self.id,self.name)

class StudyRecord(Base):
    __tablename__='student_record'
    id=Column(Integer,primary_key=True)
    score=Column(Integer,nullable=False)
    user_id=Column(Integer,ForeignKey('user.id'))


    user_rel=relationship('User',backref='my_study_record')#可以直接联查User，User也可以通过my_study_record来联查
    def __repr__(self):
        return '%s,%s'%(self.id,self.user_rel.name)



if __name__ == '__main__':
    Base.metadata.create_all(engine)  # 创建表结构，已存在的表不会重新建立，如果修改了表结构，执行也不会更新表