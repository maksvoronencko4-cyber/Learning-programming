COURSES = {
    "python": {
        "id": "python",
        "title": "Python",
        "icon": "🐍",
        "color": "#3776AB",
        "description": "Изучите Python с нуля — от переменных до ООП",
        "lessons": [
            {
                "title": "Привет, Python!",
                "theory": """
<h3>Что такое Python?</h3>
<p>Python — это высокоуровневый язык программирования, созданный Гвидо ван Россумом в 1991 году.</p>

<h3>Первая программа</h3>
<pre><code>print("Привет, мир!")</code></pre>
<p>Функция <code>print()</code> выводит текст в консоль.</p>

<h3>Комментарии</h3>
<pre><code># Это комментарий
print("Это код")</code></pre>
                """,
                "questions": [
                    {"question": "Какая функция выводит текст?", "options": ["echo", "print", "write", "show"], "answer": "print"},
                    {"question": "Символ комментария?", "options": ["//", "#", "/*", "--"], "answer": "#"},
                    {"question": "Что выведет print('Hello')?", "options": ["Hello", "'Hello'", "Ошибка", "Ничего"], "answer": "Hello"}
                ]
            },
            {
                "title": "Переменные и типы данных",
                "theory": """
<h3>Переменные</h3>
<pre><code>name = "Алиса"
age = 25
height = 1.68
is_student = True</code></pre>

<h3>Основные типы</h3>
<ul>
    <li><code>str</code> — строка</li>
    <li><code>int</code> — целое число</li>
    <li><code>float</code> — дробное число</li>
    <li><code>bool</code> — логический тип</li>
</ul>
                """,
                "questions": [
                    {"question": "Тип 3.14?", "options": ["int", "str", "float", "bool"], "answer": "float"},
                    {"question": "Тип True?", "options": ["int", "str", "float", "bool"], "answer": "bool"},
                    {"question": "Тип числа 5?", "options": ["str", "int", "float", "bool"], "answer": "int"}
                ]
            },
            {
                "title": "Арифметические операции",
                "theory": """
<h3>Операторы</h3>
<pre><code>a = 10
b = 3
print(a + b)   # 13
print(a - b)   # 7
print(a * b)   # 30
print(a / b)   # 3.33...
print(a // b)  # 3
print(a % b)   # 1
print(a ** b)  # 1000</code></pre>
                """,
                "questions": [
                    {"question": "Что вернёт 10 % 3?", "options": ["3", "1", "0", "10"], "answer": "1"},
                    {"question": "Что вернёт 2 ** 4?", "options": ["8", "16", "6", "24"], "answer": "16"},
                    {"question": "Что вернёт 7 // 2?", "options": ["3.5", "3", "4", "2"], "answer": "3"}
                ]
            },
            {
                "title": "Условия if/else",
                "theory": """
<h3>Условный оператор</h3>
<pre><code>age = 18
if age >= 18:
    print("Совершеннолетний")
else:
    print("Несовершеннолетний")</code></pre>

<h3>elif</h3>
<pre><code>score = 85
if score >= 90:
    print("Отлично")
elif score >= 70:
    print("Хорошо")
else:
    print("Нужно подтянуть")</code></pre>
                """,
                "questions": [
                    {"question": "Что выведет if 5 > 3: print('Да')?", "options": ["Да", "Нет", "Ошибка", "Ничего"], "answer": "Да"},
                    {"question": "Оператор И?", "options": ["or", "and", "not", "if"], "answer": "and"},
                    {"question": "Что проверяет elif?", "options": ["Альтернативное условие", "Цикл", "Ошибку", "Тип"], "answer": "Альтернативное условие"}
                ]
            },
            {
                "title": "Циклы",
                "theory": """
<h3>Цикл for</h3>
<pre><code>for i in range(5):
    print(i)  # 0, 1, 2, 3, 4</code></pre>

<h3>Цикл while</h3>
<pre><code>count = 0
while count < 5:
    print(count)
    count += 1</code></pre>
                """,
                "questions": [
                    {"question": "range(3) даёт?", "options": ["1,2,3", "0,1,2", "0,1,2,3", "3"], "answer": "0,1,2"},
                    {"question": "Что делает break?", "options": ["Останавливает цикл", "Пропускает итерацию", "Повторяет цикл", "Ничего"], "answer": "Останавливает цикл"},
                    {"question": "Сколько раз for i in range(1,4)?", "options": ["4", "3", "2", "1"], "answer": "3"}
                ]
            }
        ]
    },
    "javascript": {
        "id": "javascript",
        "title": "JavaScript",
        "icon": "🌐",
        "color": "#F7DF1E",
        "description": "Язык веба — от основ до функций",
        "lessons": [
            {
                "title": "Привет, JavaScript!",
                "theory": """
<h3>Вывод в консоль</h3>
<pre><code>console.log("Привет!");</code></pre>

<h3>Переменные</h3>
<pre><code>let name = "JS";
const PI = 3.14;</code></pre>
                """,
                "questions": [
                    {"question": "Функция вывода?", "options": ["print", "console.log", "echo", "write"], "answer": "console.log"},
                    {"question": "Неизменяемая переменная?", "options": ["let", "var", "const", "static"], "answer": "const"},
                    {"question": "Тип let x;?", "options": ["null", "undefined", "string", "number"], "answer": "undefined"}
                ]
            },
            {
                "title": "Условия и циклы",
                "theory": """
<h3>if/else</h3>
<pre><code>if (age >= 18) {
    console.log("OK");
} else {
    console.log("No");
}</code></pre>

<h3>Цикл for</h3>
<pre><code>for (let i = 0; i < 5; i++) {
    console.log(i);
}</code></pre>
                """,
                "questions": [
                    {"question": "Что вернёт 5 === '5'?", "options": ["true", "false", "5", "Ошибка"], "answer": "false"},
                    {"question": "i++ означает?", "options": ["i = i + 1", "i = i - 1", "i = 0", "i * 2"], "answer": "i = i + 1"},
                    {"question": "Скобки для блока кода?", "options": ["()", "[]", "{}", "<>"], "answer": "{}"}
                ]
            }
        ]
    },
    "html_css": {
        "id": "html_css",
        "title": "HTML & CSS",
        "icon": "🎨",
        "color": "#E44D26",
        "description": "Создавайте веб-страницы",
        "lessons": [
            {
                "title": "Основы HTML",
                "theory": """
<h3>Структура</h3>
<pre><code>&lt;!DOCTYPE html&gt;
&lt;html&gt;
&lt;head&gt;
    &lt;title&gt;Сайт&lt;/title&gt;
&lt;/head&gt;
&lt;body&gt;
    &lt;h1&gt;Привет!&lt;/h1&gt;
&lt;/body&gt;
&lt;/html&gt;</code></pre>
                """,
                "questions": [
                    {"question": "Главный заголовок?", "options": ["title", "h1", "header", "head"], "answer": "h1"},
                    {"question": "Контент страницы?", "options": ["head", "body", "html", "meta"], "answer": "body"},
                    {"question": "Тег ссылки?", "options": ["link", "a", "href", "url"], "answer": "a"}
                ]
            },
            {
                "title": "Основы CSS",
                "theory": """
<h3>Синтаксис</h3>
<pre><code>h1 {
    color: blue;
    font-size: 24px;
}

.класс {
    background: #f0f0f0;
}</code></pre>
                """,
                "questions": [
                    {"question": "Свойство цвета текста?", "options": ["font-color", "text-color", "color", "bg"], "answer": "color"},
                    {"question": "Символ класса?", "options": ["#", ".", "@", "&"], "answer": "."},
                    {"question": "Внутренний отступ?", "options": ["margin", "padding", "border", "gap"], "answer": "padding"}
                ]
            }
        ]
    }
}


def get_course(course_id):
    return COURSES.get(course_id)


def get_all_courses():
    return COURSES


def get_lesson(course_id, lesson_index):
    course = get_course(course_id)
    if course and 0 <= lesson_index < len(course['lessons']):
        return course['lessons'][lesson_index]
    return None
