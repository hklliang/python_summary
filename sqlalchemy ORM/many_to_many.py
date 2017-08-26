#一本书可以有多个作者，一个作者又可以出版多本书


from sqlalchemy import Table, Column, Integer,String,DATE, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


Base = declarative_base()

book_m2m_author = Table('book_m2m_author', Base.metadata,
                        Column('book_id',Integer,ForeignKey('books.id')),
                        Column('author_id',Integer,ForeignKey('authors.id')),
                        )

class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer,primary_key=True)
    name = Column(String(64))
    pub_date = Column(DATE)
    authors = relationship('Author',secondary=book_m2m_author,backref='books')

    def __repr__(self):
        return self.name

class Author(Base):
    __tablename__ = 'authors'
    id = Column(Integer, primary_key=True)
    name = Column(String(32))

    def __repr__(self):
        return self.name



"""
Session_class = sessionmaker(bind=engine) #创建与数据库的会话session class ,注意,这里返回给session的是个class,不是实例
s = Session_class() #生成session实例
 
b1 = Book(name="跟Alex学Python")
b2 = Book(name="跟Alex学把妹")
b3 = Book(name="跟Alex学装逼")
b4 = Book(name="跟Alex学开车")
 
a1 = Author(name="Alex")
a2 = Author(name="Jack")
a3 = Author(name="Rain")
 
b1.authors = [a1,a2]
b2.authors = [a1,a2,a3]
 
s.add_all([b1,b2,b3,b4,a1,a2,a3])
 
s.commit()


"""