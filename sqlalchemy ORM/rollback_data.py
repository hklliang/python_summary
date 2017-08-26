from create_table import Session,User

my_user = Session.query(User).filter_by(id=1).first()

fake_user = User(name='Rain', password='12345')
Session.add(fake_user)

print(Session.query(User).filter(User.name.in_(['Jack', 'rain'])).all())  # 这时看session里有你刚添加和修改的数据

Session.rollback()  # 此时你rollback一下

print(Session.query(User).filter(User.name.in_(['Jack', 'rain'])).all())  # 再查就发现刚才添加的数据没有了。

#没有commit，再内存中有，但是数据库里没有，如果rollback，那么内存中也不会有