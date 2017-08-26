
from create_table import User,Session




user_obj = User(name="alex", password="alex3714")  # 生成你要创建的数据对象
print(user_obj.name, user_obj.id)  # 此时还没创建对象呢，不信你打印一下id发现还是None

Session.add(user_obj)  # 把要创建的数据对象添加到这个session里， 一会统一创建
print(user_obj.name, user_obj.id)  # 此时也依然还没创建


#Session.add_all([])
Session.commit()  # 现此才统一提交，创建数据