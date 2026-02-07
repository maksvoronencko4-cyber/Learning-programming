from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()


# Таблица дружбы
friendships = db.Table('friendships',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('friend_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('created_at', db.DateTime, default=datetime.utcnow)
)


class FriendRequest(db.Model):
    __tablename__ = 'friend_requests'

    id = db.Column(db.Integer, primary_key=True)
    from_user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    to_user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, accepted, rejected
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    from_user = db.relationship('User', foreign_keys=[from_user_id], backref='sent_requests')
    to_user = db.relationship('User', foreign_keys=[to_user_id], backref='received_requests')


class Message(db.Model):
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    sender = db.relationship('User', foreign_keys=[sender_id], backref='sent_messages')
    receiver = db.relationship('User', foreign_keys=[receiver_id], backref='received_messages')

    def to_dict(self):
        return {
            'id': self.id,
            'sender_id': self.sender_id,
            'sender_name': self.sender.username,
            'receiver_id': self.receiver_id,
            'content': self.content,
            'is_read': self.is_read,
            'created_at': self.created_at.strftime('%H:%M'),
            'created_date': self.created_at.strftime('%d.%m.%Y'),
        }


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    bio = db.Column(db.String(200), default='')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    progress = db.relationship('UserProgress', backref='user', lazy=True)

    friends = db.relationship(
        'User',
        secondary=friendships,
        primaryjoin=(friendships.c.user_id == id),
        secondaryjoin=(friendships.c.friend_id == id),
        lazy='dynamic'
    )

    def get_course_progress(self, course_id):
        return UserProgress.query.filter_by(
            user_id=self.id, course_id=course_id
        ).first()

    def get_all_progress(self):
        return {p.course_id: p for p in self.progress}

    def is_friend(self, user):
        return self.friends.filter(
            friendships.c.friend_id == user.id
        ).count() > 0

    def add_friend(self, user):
        if not self.is_friend(user):
            self.friends.append(user)
            user.friends.append(self)

    def remove_friend(self, user):
        if self.is_friend(user):
            self.friends.remove(user)
            user.friends.remove(self)

    def get_friends_list(self):
        return self.friends.all()

    def get_pending_requests(self):
        return FriendRequest.query.filter_by(
            to_user_id=self.id, status='pending'
        ).all()

    def get_pending_count(self):
        return FriendRequest.query.filter_by(
            to_user_id=self.id, status='pending'
        ).count()

    def get_unread_messages_count(self):
        return Message.query.filter_by(
            receiver_id=self.id, is_read=False
        ).count()

    def get_unread_from(self, user_id):
        return Message.query.filter_by(
            sender_id=user_id, receiver_id=self.id, is_read=False
        ).count()

    def has_sent_request_to(self, user):
        return FriendRequest.query.filter_by(
            from_user_id=self.id, to_user_id=user.id, status='pending'
        ).count() > 0

    def has_request_from(self, user):
        return FriendRequest.query.filter_by(
            from_user_id=user.id, to_user_id=self.id, status='pending'
        ).count() > 0


class UserProgress(db.Model):
    __tablename__ = 'user_progress'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    course_id = db.Column(db.String(50), nullable=False)
    current_lesson = db.Column(db.Integer, default=0)
    completed_lessons = db.Column(db.Text, default='')
    passed_tests = db.Column(db.Text, default='')
    last_accessed = db.Column(db.DateTime, default=datetime.utcnow)
    started_at = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (
        db.UniqueConstraint('user_id', 'course_id', name='unique_user_course'),
    )

    def get_completed_list(self):
        if not self.completed_lessons:
            return []
        return [int(x) for x in self.completed_lessons.split(',') if x]

    def add_completed(self, lesson_index):
        completed = self.get_completed_list()
        if lesson_index not in completed:
            completed.append(lesson_index)
            self.completed_lessons = ','.join(str(x) for x in sorted(completed))
        return completed

    def get_passed_tests_list(self):
        if not self.passed_tests:
            return []
        return [int(x) for x in self.passed_tests.split(',') if x]

    def add_passed_test(self, lesson_index):
        passed = self.get_passed_tests_list()
        if lesson_index not in passed:
            passed.append(lesson_index)
            self.passed_tests = ','.join(str(x) for x in sorted(passed))
        return passed

    def completion_percent(self, total_lessons):
        if total_lessons == 0:
            return 0
        completed = len(self.get_completed_list())
        passed = len(self.get_passed_tests_list())
        total_items = total_lessons * 2
        done_items = completed + passed
        return int(done_items / total_items * 100)