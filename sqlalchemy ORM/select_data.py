from create_table import Session,User,StudyRecord

# user=Session.query(User).filter_by(id=1)
# user=Session.query(User).filter(User.id==1)
#User.name.like('al%')
#User.name.in_(['df','sdf'])
#
from sqlalchemy import func
print(Session.query(func.count(User.name),User.name).group_by(User.name).all())
user=Session.query(User).filter(User.id==1).filter(User.name=='jack')
print(user)
print(user.all())
print(user.first())
print(user.count())
print(user.first().my_study_record)

print(Session.query(User,StudyRecord).filter(User.id==1).filter(User.name=='jack'))