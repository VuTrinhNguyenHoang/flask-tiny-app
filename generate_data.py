import random
import uuid
from faker import Faker
from website import create_app, db
from website.models import User, Post
from werkzeug.security import generate_password_hash

fake = Faker()

NUM_USERS = 20
POSTS_PER_USER = 20

app = create_app()

def unique_slug():
    while True:
        new_slug = str(uuid.uuid4())[:8]
        if not Post.query.filter_by(slug=new_slug).first():
            return new_slug

with app.app_context():
    db.session.query(Post).delete()
    db.session.query(User).delete()
    db.session.commit()

    print('Đang tạo dữ liệu giả lập...')

    user = User(
        username='admin',
        email='admin@gmail.com',
        password=generate_password_hash('admin', method='pbkdf2:sha256'),
        is_admin=True
    )
    db.session.add(user)

    users = []
    for _ in range(NUM_USERS):
        user = User(
            username=fake.user_name(),
            email=fake.unique.email(),
            password=generate_password_hash('test123', method='pbkdf2:sha256')
        )
        db.session.add(user)
        users.append(user)
    
    db.session.commit()

    for user in users:
        for _ in range(POSTS_PER_USER):
            post = Post(
                user_id=user.id,
                title=fake.sentence(nb_words=4),
                content=fake.paragraph(nb_sentences=50),
                slug=unique_slug()
            )
            db.session.add(post)
    
    db.session.commit()
    print('Dữ liệu giả lập đã được tạo thành công!')