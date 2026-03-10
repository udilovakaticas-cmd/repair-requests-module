from flask import Flask, render_template, request, redirect, url_for, session
import firebase_admin
from firebase_admin import credentials, db

app = Flask(__name__)
app.secret_key = 'super_secret_key'  # нужно для session

# --- Настройка Firebase ---
cred = credentials.Certificate('firebase_key.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://bd-kiberone-default-rtdb.firebaseio.com/'
})

# --- Главная страница ---
@app.route('/')
def index():
    return render_template('index.html')

# --- Вход ученика ---
@app.route('/login_student', methods=['GET', 'POST'])
def login_student():
    if request.method == 'POST':
        first_name = request.form['first_name'].strip()
        last_name = request.form['last_name'].strip()

        # Проверяем в базе, есть ли такой ученик
        ref = db.reference('students')
        students = ref.order_by_child('first_name').equal_to(first_name).get()

        # Ищем по фамилии среди найденных
        student_id = None
        for key, value in students.items():
            if value.get('last_name') == last_name:
                student_id = key
                break

        if student_id:
            # сохраняем ID в сессию
            session['student_id'] = student_id
            return redirect(url_for('student_cabinet'))
        else:
            return "Ученик не найден. Проверьте имя и фамилию.", 400

    return render_template('login_student.html')


# --- Личный кабинет ученика ---
@app.route('/student_cabinet')
def student_cabinet():
    student_id = session.get('student_id')
    if not student_id:
        return "Student ID не найден в сессии", 400

    ref = db.reference(f'students/{student_id}')
    student = ref.get()

    if not student:
        return "Данные ученика не найдены", 404

    return render_template('student_cabinet.html', student=student, student_id=student_id)


# --- Обновление аватара ---
@app.route('/update_avatar', methods=['POST'])
def update_avatar():
    student_id = session.get('student_id')
    new_avatar = request.form.get('avatar')

    if not student_id or not new_avatar:
        return "Ошибка: данные не получены", 400

    ref = db.reference(f'students/{student_id}')
    ref.update({'avatar': new_avatar})

    return redirect(url_for('student_cabinet'))

@app.route('/test/<level_id>', methods=['GET', 'POST'])
def test(level_id):
    student_id = session.get("student_id")
    if not student_id:
        return "Student ID не найден в сессии", 400

    # --- Получаем данные теста ---
    ref = db.reference(f'levels_test/level_{level_id}')
    test_data = ref.get()

    if not test_data:
        return "Тест не найден", 404

    # --- Список вопросов ---
    questions = list(test_data.get("tasks", {}).values())
    current_index = session.get(f'level_{level_id}_index', 0)

    # --- Если отправлен ответ ---
    if request.method == 'POST':
        answer = request.form.get("answer")
        answer_checked = True

        correct = questions[current_index]["correct"]
        wrong = (int(answer) != correct)

        # Если верно — переход к следующему вопросу
        if not wrong:
            current_index += 1
            session[f'level_{level_id}_index'] = current_index

        # Если вопросы закончились — завершаем тест
        if current_index >= len(questions):
            session.pop(f'level_{level_id}_index', None)
            return redirect(url_for('student_cabinet'))

        # Возвращаем шаблон с флагами
        return render_template(
            "test.html",
            question=questions[current_index],
            level_id=level_id,
            index=current_index+1,
            total=len(questions),
            answer_checked=True,
            wrong=wrong
        )

    # --- GET запрос ---
    if current_index < len(questions):
        return render_template(
            "test.html",
            question=questions[current_index],
            level_id=level_id,
            index=current_index+1,
            total=len(questions),
            answer_checked=False
        )
    else:
        session.pop(f'level_{level_id}_index', None)
        return redirect(url_for('student_cabinet'))

@app.route('/login_teacher', methods=['GET', 'POST'])
def login_teacher():
    if request.method == 'POST':
        login = request.form.get('login')
        password = request.form.get('password')

        # Получаем всех пользователей из Firebase
        ref = db.reference('users')
        users_data = ref.get() or {}

        # Ищем пользователя с ролью teacher
        for user_id, user in users_data.items():
            if user.get('login') == login and user.get('password') == password and user.get('role') == 'teacher':
                session['teacher_id'] = user_id
                return redirect(url_for('teacher_cabinet'))

        # Если не найдено совпадение
        return render_template('login_teacher.html', error="Неверный логин или пароль")

    # GET-запрос
    return render_template('login_teacher.html')

@app.route('/teacher_cabinet', methods=['GET', 'POST'])
def teacher_cabinet():
    teacher_id = session.get('teacher_id')
    if not teacher_id:
        return redirect(url_for('login_teacher'))

    # Получаем данные учителя
    teacher_ref = db.reference(f'users/{teacher_id}')
    teacher_data = teacher_ref.get()

    # Получаем тесты и учеников
    tests_ref = db.reference('levels_test')
    tests = tests_ref.get() or {}

    students_ref = db.reference('users')
    students = {uid: s for uid, s in (students_ref.get() or {}).items() if s.get('role') == 'student'}

    return render_template('teacher_cabinet.html', teacher=teacher_data, tests=tests, students=students)


# --- Добавление нового теста ---
@app.route('/add_test', methods=['POST'])
def add_test():
    teacher_id = session.get('teacher_id')
    if not teacher_id:
        return redirect(url_for('login_teacher'))

    test_name = request.form.get('test_name')
    if test_name:
        ref = db.reference('levels_test')
        new_test_ref = ref.push({
            'name': test_name,
            'tasks': {}  # Пока пустой список заданий
        })
    return redirect(url_for('teacher_cabinet'))


# --- Добавление нового ученика ---
@app.route('/add_student', methods=['POST'])
def add_student():
    teacher_id = session.get('teacher_id')
    if not teacher_id:
        return redirect(url_for('login_teacher'))

    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    login = request.form.get('login')
    password = request.form.get('password')

    if all([first_name, last_name, login, password]):
        ref = db.reference('users')
        ref.push({
            'first_name': first_name,
            'last_name': last_name,
            'login': login,
            'password': password,
            'role': 'student'
        })
    return redirect(url_for('teacher_cabinet'))


# --- Выход из кабинета ---
@app.route('/logout_teacher')
def logout_teacher():
    session.pop('teacher_id', None)
    return redirect(url_for('login_teacher'))

@app.route('/login_admin', methods=['GET', 'POST'])
def login_admin():
    if request.method == 'POST':
        login = request.form.get('login')
        password = request.form.get('password')

        users_ref = db.reference('users')
        users = users_ref.get() or {}

        for user_id, user in users.items():
            if user.get('login') == login and user.get('password') == password and user.get('role') == 'admin':
                session['admin_id'] = user_id
                return redirect(url_for('admin_cabinet'))

        # Неверный логин/пароль
        return render_template('login_admin.html', error="Неверный логин или пароль")

    return render_template('login_admin.html')


# Кабинет администратора
@app.route('/admin_cabinet', methods=['GET'])
def admin_cabinet():
    admin_id = session.get('admin_id')
    if not admin_id:
        return redirect(url_for('login_admin'))

    # Данные администратора
    admin_ref = db.reference(f'users/{admin_id}')
    admin_data = admin_ref.get()

    # Все пользователи
    users_ref = db.reference('users')
    users = users_ref.get() or {}

    # Все тесты
    tests_ref = db.reference('levels_test')
    tests = tests_ref.get() or {}

    tests_ref = db.reference('students')
    students = tests_ref.get() or {}

    return render_template('admin_cabinet.html',
                           admin=admin_data,
                           users=users,
                           students=students,  # <-- добавляем студентов
                           tests=tests)



    @app.route('/admin/users')
    @login_required
    def manage_users():

        role_filter = request.args.get('role', 'all')
        search_query = request.args.get('search', '')

        query = User.query
        if role_filter != 'all':
            query = query.filter_by(role=role_filter)
        if search_query:
            query = query.filter(User.fio.ilike(f'%{search_query}%'))

        users = query.all()
        return render_template('admin/users.html', users=users)



@app.route('/admin/users/bulk_delete', methods=['POST'])
def bulk_delete():
    user_ids = request.form.getlist('selected_users')
    User.query.filter(User.id.in_(user_ids)).delete(synchronize_session=False)
    db.session.commit()
    return redirect(url_for('manage_users'))

# Выход администратора
@app.route('/logout_admin')
def logout_admin():
    session.pop('admin_id', None)
    return redirect(url_for('login_admin'))

if __name__ == '__main__':
    app.run(debug=True)
