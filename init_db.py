from app import app, db
from models import User

with app.app_context():
    db.create_all()
    print('✅ テーブルを作成しました')
    
    admin = User(
        email='admin@example.com',
        username='admin',
        name='システム管理者',
        email_verified=True
    )
    admin.set_password('Admin@12345')
    db.session.add(admin)
    db.session.commit()
    print('✅ 管理者ユーザーを作成しました')
    print('Email: admin@example.com')
    print('Password: Admin@12345')