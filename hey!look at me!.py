"""
《数据库相关操作》

#必须要在command prompt里进行下述操作
#启动flask shell的必要三步骤
>>> set FLASK_APP=manage.py
>>> set FLASK_ENV=development
>>> flask shell

#重置数据库（仅在需要时进行该操作）：删除data.sqlite文件，再在右侧的数据库里移除所有数据库确保空
>>> from app.models import db
>>> db.create_all()  #等一会之后就会创建出data.sqlite文件， 双击后会展开配置， 双击测试链接， 再点击应用，几秒钟后再点击确定， 展开数据库检查是否成功导入

#录入Roles
>>> from app.models import db
>>> Role.insert_roles()  #双击数据库里的roles检查是否出现三种roles

#录入Category
>>> from app.models import Category
>>> Category.insert_categories()  #双击数据库里的categories检查是否出现categories
"""