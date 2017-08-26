from create_table import User,Session
user=Session.query(User).filter(User.id==1).filter(User.name=='alex').first()
user.name='jack'


Session.commit()

#