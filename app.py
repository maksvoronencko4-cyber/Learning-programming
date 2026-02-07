import os
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_login import (
    LoginManager, login_user, logout_user,
    login_required, current_user
)
from flask_bcrypt import Bcrypt
from flask_socketio import SocketIO, emit, join_room
from datetime import datetime
from models import db, User, UserProgress, FriendRequest, Message
from lessons_data import get_course, get_all_courses, get_lesson

app = Flask(__name__)

database_url = os.environ.get('DATABASE_URL', 'sqlite:///codelearn.db')
if database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-me')

db.init_app(app)
bcrypt = Bcrypt(app)
socketio = SocketIO(app, cors_allowed_origins="*")
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Пожалуйста, войдите в аккаунт'
login_manager.login_message_category = 'info'

online_users = {}


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


with app.app_context():
    db.create_all()


# ==================== ОСНОВНЫЕ СТРАНИЦЫ ====================

@app.route('/')
def index():
    courses = get_all_courses()
    return render_template('index.html', courses=courses)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        confirm = request.form.get('confirm_password', '')

        if not username or not email or not password:
            flash('Заполните все поля', 'error')
            return redirect(url_for('register'))
        if len(username) < 3:
            flash('Имя пользователя — минимум 3 символа', 'error')
            return redirect(url_for('register'))
        if len(password) < 6:
            flash('Пароль — минимум 6 символов', 'error')
            return redirect(url_for('register'))
        if password != confirm:
            flash('Пароли не совпадают', 'error')
            return redirect(url_for('register'))
        if User.query.filter_by(username=username).first():
            flash('Имя пользователя занято', 'error')
            return redirect(url_for('register'))
        if User.query.filter_by(email=email).first():
            flash('Email уже зарегистрирован', 'error')
            return redirect(url_for('register'))

        pw_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(username=username, email=email, password_hash=pw_hash)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash('Добро пожаловать, ' + username + '! 🎉', 'success')
        return redirect(url_for('dashboard'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password_hash, password):
            login_user(user, remember=True)
            flash('С возвращением, ' + user.username + '! 👋', 'success')
            return redirect(request.args.get('next') or url_for('dashboard'))
        else:
            flash('Неверное имя или пароль', 'error')

    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вы вышли из аккаунта', 'info')
    return redirect(url_for('index'))


@app.route('/dashboard')
@login_required
def dashboard():
    courses = get_all_courses()
    progress = current_user.get_all_progress()

    course_data = []
    for cid, course in courses.items():
        p = progress.get(cid)
        total = len(course['lessons'])
        completed_lessons = len(p.get_completed_list()) if p else 0
        passed_tests = len(p.get_passed_tests_list()) if p else 0
        percent = p.completion_percent(total) if p else 0
        current = p.current_lesson if p else 0
        course_data.append({
            'course': course,
            'completed_lessons': completed_lessons,
            'passed_tests': passed_tests,
            'total': total,
            'percent': percent,
            'current_lesson': current,
            'started': p is not None
        })

    pending_count = current_user.get_pending_count()
    unread_count = current_user.get_unread_messages_count()

    return render_template('dashboard.html',
                           course_data=course_data,
                           pending_count=pending_count,
                           unread_count=unread_count)


@app.route('/courses')
def courses():
    all_courses = get_all_courses()
    progress = {}
    if current_user.is_authenticated:
        progress = current_user.get_all_progress()
    return render_template('courses.html', courses=all_courses, progress=progress)


# ==================== ИЗУЧЕНИЕ ====================

@app.route('/learn/<course_id>/<int:lesson_index>')
@login_required
def learn(course_id, lesson_index):
    course = get_course(course_id)
    if not course:
        flash('Курс не найден', 'error')
        return redirect(url_for('courses'))

    lesson_data = get_lesson(course_id, lesson_index)
    if not lesson_data:
        flash('Урок не найден', 'error')
        return redirect(url_for('courses'))

    total_lessons = len(course['lessons'])
    progress = current_user.get_course_progress(course_id)

    if not progress:
        progress = UserProgress(
            user_id=current_user.id,
            course_id=course_id,
            current_lesson=lesson_index
        )
        db.session.add(progress)
        db.session.commit()

    progress.current_lesson = lesson_index
    progress.last_accessed = datetime.utcnow()
    progress.add_completed(lesson_index)
    db.session.commit()

    return render_template(
        'learn.html',
        course=course,
        lesson=lesson_data,
        lesson_index=lesson_index,
        total_lessons=total_lessons,
        completed_list=progress.get_completed_list()
    )


# ==================== ТЕСТЫ ====================

@app.route('/test/<course_id>/<int:lesson_index>', methods=['GET', 'POST'])
@login_required
def test(course_id, lesson_index):
    course = get_course(course_id)
    if not course:
        flash('Курс не найден', 'error')
        return redirect(url_for('courses'))

    lesson_data = get_lesson(course_id, lesson_index)
    if not lesson_data:
        flash('Тест не найден', 'error')
        return redirect(url_for('courses'))

    total_lessons = len(course['lessons'])
    questions = lesson_data.get('questions', [])
    total_questions = len(questions)

    progress = current_user.get_course_progress(course_id)
    if not progress:
        progress = UserProgress(
            user_id=current_user.id,
            course_id=course_id,
            current_lesson=lesson_index
        )
        db.session.add(progress)
        db.session.commit()

    result = None
    score = 0
    user_answers = {}
    answer_results = {}

    if request.method == 'POST':
        correct_count = 0
        for i, q in enumerate(questions):
            user_ans = request.form.get('q' + str(i), '').strip()
            correct_ans = q['answer'].strip()
            user_answers[i] = user_ans
            is_correct = user_ans.lower() == correct_ans.lower()
            answer_results[i] = is_correct
            if is_correct:
                correct_count += 1

        score = correct_count
        if correct_count == total_questions:
            result = 'pass'
            progress.add_passed_test(lesson_index)
            db.session.commit()
            flash('Тест пройден! ' + str(score) + '/' + str(total_questions) + ' ✅', 'success')
        else:
            result = 'fail'
            flash('Не пройден: ' + str(score) + '/' + str(total_questions), 'error')

    passed_list = progress.get_passed_tests_list()

    return render_template(
        'test.html',
        course=course,
        lesson=lesson_data,
        lesson_index=lesson_index,
        total_lessons=total_lessons,
        result=result,
        score=score,
        total_questions=total_questions,
        user_answers=user_answers,
        answer_results=answer_results,
        passed_list=passed_list
    )


@app.route('/tests/<course_id>')
@login_required
def tests_list(course_id):
    course = get_course(course_id)
    if not course:
        flash('Курс не найден', 'error')
        return redirect(url_for('courses'))

    progress = current_user.get_course_progress(course_id)
    passed_list = progress.get_passed_tests_list() if progress else []
    completed_list = progress.get_completed_list() if progress else []

    return render_template(
        'tests_list.html',
        course=course,
        passed_list=passed_list,
        completed_list=completed_list
    )


# ==================== ДРУЗЬЯ ====================

@app.route('/friends')
@login_required
def friends():
    friends_list = current_user.get_friends_list()
    pending = current_user.get_pending_requests()
    courses = get_all_courses()

    friends_data = []
    for friend in friends_list:
        f_progress = friend.get_all_progress()
        total_completed = 0
        total_passed = 0
        total_lessons = 0
        for cid, course in courses.items():
            t = len(course['lessons'])
            total_lessons += t
            p = f_progress.get(cid)
            if p:
                total_completed += len(p.get_completed_list())
                total_passed += len(p.get_passed_tests_list())

        unread = current_user.get_unread_from(friend.id)
        is_online = friend.id in online_users

        friends_data.append({
            'user': friend,
            'total_completed': total_completed,
            'total_passed': total_passed,
            'total_lessons': total_lessons,
            'unread': unread,
            'is_online': is_online
        })

    return render_template('friends.html', friends_data=friends_data, pending=pending)


@app.route('/search_users', methods=['GET', 'POST'])
@login_required
def search_users():
    results = []
    query = ''

    if request.method == 'POST':
        query = request.form.get('query', '').strip()
        if len(query) >= 2:
            results = User.query.filter(
                User.username.ilike('%' + query + '%'),
                User.id != current_user.id
            ).limit(20).all()

    return render_template('search_users.html', results=results, query=query)


@app.route('/send_request/<int:user_id>')
@login_required
def send_friend_request(user_id):
    user = User.query.get_or_404(user_id)

    if user.id == current_user.id:
        flash('Нельзя добавить себя', 'error')
        return redirect(url_for('search_users'))

    if current_user.is_friend(user):
        flash(user.username + ' уже в друзьях', 'info')
        return redirect(url_for('friends'))

    if current_user.has_sent_request_to(user):
        flash('Запрос уже отправлен', 'info')
        return redirect(url_for('search_users'))

    if current_user.has_request_from(user):
        current_user.add_friend(user)
        req = FriendRequest.query.filter_by(
            from_user_id=user.id,
            to_user_id=current_user.id,
            status='pending'
        ).first()
        if req:
            req.status = 'accepted'
        db.session.commit()
        flash(user.username + ' добавлен в друзья! 🎉', 'success')
        return redirect(url_for('friends'))

    fr = FriendRequest(from_user_id=current_user.id, to_user_id=user.id)
    db.session.add(fr)
    db.session.commit()
    flash('Запрос отправлен ' + user.username, 'success')

    try:
        socketio.emit('new_request', {
            'from_user': current_user.username,
            'count': user.get_pending_count()
        }, room='user_' + str(user.id))
    except Exception:
        pass

    return redirect(url_for('search_users'))


@app.route('/accept_request/<int:request_id>')
@login_required
def accept_request(request_id):
    fr = FriendRequest.query.get_or_404(request_id)
    if fr.to_user_id != current_user.id:
        flash('Нет доступа', 'error')
        return redirect(url_for('friends'))

    fr.status = 'accepted'
    current_user.add_friend(fr.from_user)
    db.session.commit()
    flash(fr.from_user.username + ' добавлен в друзья! 🎉', 'success')
    return redirect(url_for('friends'))


@app.route('/reject_request/<int:request_id>')
@login_required
def reject_request(request_id):
    fr = FriendRequest.query.get_or_404(request_id)
    if fr.to_user_id != current_user.id:
        flash('Нет доступа', 'error')
        return redirect(url_for('friends'))

    fr.status = 'rejected'
    db.session.commit()
    flash('Запрос отклонён', 'info')
    return redirect(url_for('friends'))


@app.route('/remove_friend/<int:user_id>')
@login_required
def remove_friend(user_id):
    user = User.query.get_or_404(user_id)
    if current_user.is_friend(user):
        current_user.remove_friend(user)
        db.session.commit()
        flash(user.username + ' удалён из друзей', 'info')
    return redirect(url_for('friends'))


# ==================== ЧАТ ====================

@app.route('/chat/<int:user_id>')
@login_required
def chat(user_id):
    other_user = User.query.get_or_404(user_id)

    if not current_user.is_friend(other_user):
        flash('Можно писать только друзьям', 'error')
        return redirect(url_for('friends'))

    try:
        Message.query.filter_by(
            sender_id=user_id,
            receiver_id=current_user.id,
            is_read=False
        ).update({'is_read': True})
        db.session.commit()
    except Exception:
        db.session.rollback()

    messages = Message.query.filter(
        db.or_(
            db.and_(
                Message.sender_id == current_user.id,
                Message.receiver_id == user_id
            ),
            db.and_(
                Message.sender_id == user_id,
                Message.receiver_id == current_user.id
            )
        )
    ).order_by(Message.created_at.asc()).limit(200).all()

    is_online = user_id in online_users

    return render_template(
        'chat.html',
        other_user=other_user,
        messages=messages,
        is_online=is_online
    )


@app.route('/chat_list')
@login_required
def chat_list():
    friends_list = current_user.get_friends_list()
    chats = []

    for friend in friends_list:
        last_msg = Message.query.filter(
            db.or_(
                db.and_(
                    Message.sender_id == current_user.id,
                    Message.receiver_id == friend.id
                ),
                db.and_(
                    Message.sender_id == friend.id,
                    Message.receiver_id == current_user.id
                )
            )
        ).order_by(Message.created_at.desc()).first()

        unread = current_user.get_unread_from(friend.id)
        is_online = friend.id in online_users

        chats.append({
            'user': friend,
            'last_message': last_msg,
            'unread': unread,
            'is_online': is_online
        })

    chats.sort(
        key=lambda x: x['last_message'].created_at if x['last_message'] else datetime.min,
        reverse=True
    )

    return render_template('chat_list.html', chats=chats)


# ==================== ПРОФИЛЬ ====================

@app.route('/profile')
@login_required
def profile():
    return view_profile(current_user.id)


@app.route('/user/<int:user_id>')
@login_required
def view_user_profile(user_id):
    return view_profile(user_id)


def view_profile(user_id):
    user = User.query.get_or_404(user_id)
    courses = get_all_courses()
    progress = user.get_all_progress()

    total_completed = 0
    total_passed = 0
    total_lessons = 0
    stats = []

    for cid, course in courses.items():
        t = len(course['lessons'])
        total_lessons += t
        p = progress.get(cid)
        c = len(p.get_completed_list()) if p else 0
        pt = len(p.get_passed_tests_list()) if p else 0
        total_completed += c
        total_passed += pt

        percent = 0
        test_percent = 0
        if t > 0:
            percent = int(c / t * 100)
            test_percent = int(pt / t * 100)

        stats.append({
            'course': course,
            'completed': c,
            'passed_tests': pt,
            'total': t,
            'percent': percent,
            'test_percent': test_percent
        })

    is_own = (user.id == current_user.id)
    is_friend = False
    has_sent = False
    has_received = False

    if not is_own:
        is_friend = current_user.is_friend(user)
        has_sent = current_user.has_sent_request_to(user)
        has_received = current_user.has_request_from(user)

    is_online = user.id in online_users

    return render_template(
        'profile.html',
        profile_user=user,
        stats=stats,
        total_completed=total_completed,
        total_passed=total_passed,
        total_lessons=total_lessons,
        is_own=is_own,
        is_friend=is_friend,
        has_sent=has_sent,
        has_received=has_received,
        is_online=is_online
    )


# ==================== SOCKETIO ====================

@socketio.on('connect')
def handle_connect():
    if current_user.is_authenticated:
        online_users[current_user.id] = request.sid
        join_room('user_' + str(current_user.id))

        try:
            current_user.last_seen = datetime.utcnow()
            db.session.commit()
        except Exception:
            db.session.rollback()

        try:
            for friend in current_user.get_friends_list():
                if friend.id in online_users:
                    emit('user_online',
                         {'user_id': current_user.id},
                         room='user_' + str(friend.id))
        except Exception:
            pass


@socketio.on('disconnect')
def handle_disconnect():
    if current_user.is_authenticated:
        online_users.pop(current_user.id, None)

        try:
            current_user.last_seen = datetime.utcnow()
            db.session.commit()
        except Exception:
            db.session.rollback()

        try:
            for friend in current_user.get_friends_list():
                if friend.id in online_users:
                    emit('user_offline',
                         {'user_id': current_user.id},
                         room='user_' + str(friend.id))
        except Exception:
            pass


@socketio.on('send_message')
def handle_send_message(data):
    if not current_user.is_authenticated:
        return

    receiver_id = data.get('receiver_id')
    content = data.get('content', '').strip()

    if not content or not receiver_id:
        return

    if len(content) > 2000:
        content = content[:2000]

    try:
        receiver = User.query.get(receiver_id)
        if not receiver or not current_user.is_friend(receiver):
            return

        msg = Message(
            sender_id=current_user.id,
            receiver_id=receiver_id,
            content=content
        )
        db.session.add(msg)
        db.session.commit()

        msg_data = msg.to_dict()

        emit('new_message', msg_data, room='user_' + str(current_user.id))

        if receiver_id in online_users:
            emit('new_message', msg_data, room='user_' + str(receiver_id))

    except Exception:
        db.session.rollback()


@socketio.on('typing')
def handle_typing(data):
    if not current_user.is_authenticated:
        return

    receiver_id = data.get('receiver_id')
    if receiver_id and receiver_id in online_users:
        try:
            emit('user_typing', {
                'user_id': current_user.id,
                'username': current_user.username
            }, room='user_' + str(receiver_id))
        except Exception:
            pass


if __name__ == '__main__':

    socketio.run(app, debug=True, allow_unsafe_werkzeug=True)
