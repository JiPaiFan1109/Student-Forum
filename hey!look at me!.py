'''
Role.insert_roles()
Role.query.all()
'''

'''
default_role = Role.query.filter_by(default=True).first()
for u in User.query.all():
    if u.role is None:
        u.role = default_role

db.session.commit()
'''