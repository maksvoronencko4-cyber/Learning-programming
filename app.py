import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_bcrypt import Bcrypt
from datetime import datetime
from models import db, User, UserProgress, FriendRequest, Message
from lessons_data import get_course, get_all_courses, get_lesson

app = Flask(__name__)

# Database config
database_url = os.environ.get('DATABASE_URL', 'sqlite:///codelearn.db')
if database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

db.init_app(app)
bcrypt = Bcrypt(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


with app.app_context():
    db.create_all()


# ========== ROUTES ==========

@app.route('/')
def index():
    return render_template('index.html', courses=get_all_courses())


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
        if password != confirm:
            flash('Пароли не совпадают', 'error')
            return redirect(url_for('register'))
        if User.query.filter_by(username=username).first():
            flash('Имя занято', 'error')
            return redirect(url_for('register'))

        user = User(
            username=username,
            email=email,
            password_hash=bcrypt.generate_password_hash(password).decode('utf-8')
        )
        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash('Добро пожаловать!', 'success')
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
            flash('С возвращением!', 'success')
            return redirect(url_for('dashboard'))
        flash('Неверные данные', 'error')

    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
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
        completed = len(p.get_completed_list()) if p else 0
        passed = len(p.get_passed_tests_list()) if p else 0
        percent = p.completion_percent(total) if p else 0
        course_data.append({
            'course': course,
            'completed_lessons': completed,
            'passed_tests': passed,
            'total': total,
            'percent': percent,
            'current_lesson': p.current_lesson if p else 0,
            'started': p is not None
        })

    return render_template('dashboard.html', course_data=course_data)


@app.route('/courses')
def courses():
    progress = current_user.get_all_progress() if current_user.is_authenticated else {}
    return render_template('courses.html', courses=get_all_courses(), progress=progress)


@app.route('/learn/<course_id>/<int:lesson_index>')
@login_required
def learn(course_id, lesson_index):
    course = get_course(course_id)
    if not course:
        return redirect(url_for('courses'))

    lesson = get_lesson(course_id, lesson_index)
    if not lesson:
        return redirect(url_for('courses'))

    progress = current_user.get_course_progress(course_id)
    if not progress:
        progress = UserProgress(user_id=current_user.id, course_id=course_id)
        db.session.add(progress)

    progress.current_lesson = lesson_index
    progress.add_completed(lesson_index)
    progress.last_accessed = datetime.utcnow()
    db.session.commit()

    return render_template(
        'learn.html',
        course=course,
        lesson=lesson,
        lesson_index=lesson_index,
        total_lessons=len(course['lessons']),
        completed_list=progress.get_completed_list()
    )


@app.route('/test/<course_id>/<int:lesson_index>', methods=['GET', 'POST'])
@login_required
def test(course_id, lesson_index):
    course = get_course(course_id)
    lesson = get_lesson(course_id, lesson_index)
    if not course or not lesson:
        return redirect(url_for('courses'))

    questions = lesson.get('questions', [])
    progress = current_user.get_course_progress(course_id)
    if not progress:
        progress = UserProgress(user_id=current_user.id, course_id=course_id)
        db.session.add(progress)
        db.session.commit()

    result = None
    score = 0
    user_answers = {}
    answer_results = {}

    if request.method == 'POST':
        correct = 0
        for i, q in enumerate(questions):
            ans = request.form.get('q' + str(i), '').strip()
            user_answers[i] = ans
            is_right = ans.lower() == q['answer'].lower()
            answer_results[i] = is_right
            if is_right:
                correct += 1

        score = correct
        if score == len(questions):
            result = 'pass'
            progress.add_passed_test(lesson_index)
            db.session.commit()
            flash('Тест пройден!', 'success')
        else:
            result = 'fail'
            flash('Попробуйте ещё', 'error')

    return render_template(
        'test.html',
        course=course,
        lesson=lesson,
        lesson_index=lesson_index,
        total_lessons=len(course['lessons']),
        result=result,
        score=score,
        total_questions=len(questions),
        user_answers=user_answers,
        answer_results=answer_results,
        passed_list=progress.get_passed_tests_list()
    )


@app.route('/tests/<course_id>')
@login_required
def tests_list(course_id):
    course = get_course(course_id)
    if not course:
        return redirect(url_for('courses'))

    progress = current_user.get_course_progress(course_id)
    return render_template(
        'tests_list.html',
        course=course,
        passed_list=progress.get_passed_tests_list() if progress else [],
        completed_list=progress.get_completed_list() if progress else []
    )


@app.route('/friends')
@login_required
def friends():
    friends_list = current_user.get_friends_list()
    courses = get_all_courses()
    friends_data = []

    for f in friends_list:
        p = f.get_all_progress()
        completed = sum(len(p[c].get_completed_list()) for c in courses if c in p)
        passed = sum(len(p[c].get_passed_tests_list()) for c in courses if c in p)
        friends_data.append({
            'user': f,
            'total_completed': completed,
            'total_passed': passed,
            'unread': current_user.get_unread_from(f.id),
            'is_online': False
        })

    return render_template(
        'friends.html',
        friends_data=friends_data,
        pending=current_user.get_pending_requests()
    )


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

    if user.id == current_user.id or current_user.is_friend(user):
        return redirect(url_for('friends'))

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
        flash('Добавлен в друзья!', 'success')
        return redirect(url_for('friends'))

    if not current_user.has_sent_request_to(user):
        db.session.add(FriendRequest(from_user_id=current_user.id, to_user_id=user.id))
        db.session.commit()
        flash('Запрос отправлен', 'success')

    return redirect(url_for('search_users'))


@app.route('/accept_request/<int:req_id>')
@login_required
def accept_request(req_id):
    req = FriendRequest.query.get_or_404(req_id)
    if req.to_user_id == current_user.id:
        req.status = 'accepted'
        current_user.add_friend(req.from_user)
        db.session.commit()
        flash('Добавлен в друзья!', 'success')
    return redirect(url_for('friends'))


@app.route('/reject_request/<int:req_id>')
@login_required
def reject_request(req_id):
    req = FriendRequest.query.get_or_404(req_id)
    if req.to_user_id == current_user.id:
        req.status = 'rejected'
        db.session.commit()
    return redirect(url_for('friends'))


@app.route('/remove_friend/<int:user_id>')
@login_required
def remove_friend(user_id):
    user = User.query.get_or_404(user_id)
    if current_user.is_friend(user):
        current_user.remove_friend(user)
        db.session.commit()
    return redirect(url_for('friends'))


@app.route('/chat_list')
@login_required
def chat_list():
    chats = []
    for f in current_user.get_friends_list():
        last = Message.query.filter(
            db.or_(
                db.and_(Message.sender_id == current_user.id, Message.receiver_id == f.id),
                db.and_(Message.sender_id == f.id, Message.receiver_id == current_user.id)
            )
        ).order_by(Message.created_at.desc()).first()

        chats.append({
            'user': f,
            'last_message': last,
            'unread': current_user.get_unread_from(f.id),
            'is_online': False
        })

    chats.sort(
        key=lambda x: x['last_message'].created_at if x['last_message'] else datetime.min,
        reverse=True
    )
    return render_template('chat_list.html', chats=chats)


@app.route('/chat/<int:user_id>', methods=['GET', 'POST'])
@login_required
def chat(user_id):
    other = User.query.get_or_404(user_id)

    if not current_user.is_friend(other):
        flash('Можно писать только друзьям', 'error')
        return redirect(url_for('friends'))

    if request.method == 'POST':
        content = request.form.get('message', '').strip()
        if content:
            msg = Message(sender_id=current_user.id, receiver_id=user_id, content=content[:2000])
            db.session.add(msg)
            db.session.commit()
        return redirect(url_for('chat', user_id=user_id))

    Message.query.filter_by(
        sender_id=user_id,
        receiver_id=current_user.id,
        is_read=False
    ).update({'is_read': True})
    db.session.commit()

    messages = Message.query.filter(
        db.or_(
            db.and_(Message.sender_id == current_user.id, Message.receiver_id == user_id),
            db.and_(Message.sender_id == user_id, Message.receiver_id == current_user.id)
        )
    ).order_by(Message.created_at.asc()).limit(200).all()

    return render_template('chat.html', other_user=other, messages=messages, is_online=False)


@app.route('/profile')
@login_required
def profile():
    return show_profile(current_user.id)


@app.route('/user/<int:user_id>')
@login_required
def view_user_profile(user_id):
    return show_profile(user_id)


def show_profile(uid):
    user = User.query.get_or_404(uid)
    courses = get_all_courses()
    progress = user.get_all_progress()

    stats = []
    total_c, total_p, total_l = 0, 0, 0

    for cid, c in courses.items():
        t = len(c['lessons'])
        total_l += t
        p = progress.get(cid)
        comp = len(p.get_completed_list()) if p else 0
        passed = len(p.get_passed_tests_list()) if p else 0
        total_c += comp
        total_p += passed

        stats.append({
            'course': c,
            'completed': comp,
            'passed_tests': passed,
            'total': t,
            'percent': int(comp / t * 100) if t > 0 else 0,
            'test_percent': int(passed / t * 100) if t > 0 else 0
        })

    is_own = uid == current_user.id

    return render_template(
        'profile.html',
        profile_user=user,
        stats=stats,
        total_completed=total_c,
        total_passed=total_p,
        total_lessons=total_l,
        is_own=is_own,
        is_friend=current_user.is_friend(user) if not is_own else False,
        has_sent=current_user.has_sent_request_to(user) if not is_own else False,
        has_received=current_user.has_request_from(user) if not is_own else False,
        is_online=False
    )


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
