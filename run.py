from app import create_app, db
from app.models import User
import os

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        if User.query.count() == 0:
            u = User(username=os.environ.get('APP_USER', 'admin'))
            u.set_password(os.environ.get('APP_PASS', 'password'))
            db.session.add(u)
            db.session.commit()
            print('Created default user:', u.username)
    app.run(host='0.0.0.0', port=5000, debug=True)
