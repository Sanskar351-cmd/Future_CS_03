from dotenv import load_dotenv
import os

# Load variables from .env
load_dotenv()

from app import create_app, db
from app.models import User

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        # Create a default user if none exists
        if User.query.count() == 0:
            username = os.environ.get('APP_USER', 'defaultuser')
            password = os.environ.get('APP_PASS', 'defaultpass')
            
            u = User(username=username)
            u.set_password(password)
            
            db.session.add(u)
            db.session.commit()
            print('✅ Created default user:', u.username)
    
    # Start Flask app
    app.run(host='0.0.0.0', port=5000, debug=True)

