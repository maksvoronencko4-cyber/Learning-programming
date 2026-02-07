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
<p>Python — это высокоуровневый язык программирования, созданный <strong>Гвидо ван Россумом</strong> в 1991 году.</p>

<h3>Первая программа</h3>
<pre><code>print("Привет, мир!")</code></pre>
<p>Функция <code>print()</code> выводит текст в консоль. Текст нужно заключать в кавычки.</p>

<h3>Комментарии</h3>
<pre><code># Это комментарий — Python его игнорирует
print("Это код")  # Комментарий после кода</code></pre>

<h3>Несколько print</h3>
<pre><code>print("Строка 1")
print("Строка 2")
print("Строка 3")</code></pre>
                """,
                "questions": [
                    {
                        "question": "Какая функция выводит текст на экран в Python?",
                        "options": ["echo", "print", "write", "show"],
                        "answer": "print"
                    },
                    {
                        "question": "Какой символ используется для комментариев в Python?",
                        "options": ["//", "#", "/*", "--"],
                        "answer": "#"
                    },
                    {
                        "question": "Что выведет print('Hello')?",
                        "options": ["Hello", "'Hello'", "print Hello", "Ошибка"],
                        "answer": "Hello"
                    }
                ]
            },
            {
                "title": "Переменные и типы данных",
                "theory": """
<h3>Переменные</h3>
<p>Переменная — это именованное место в памяти для хранения данных:</p>
<pre><code>name = "Алиса"
age = 25
height = 1.68
is_student = True</code></pre>

<h3>Основные типы данных</h3>
<ul>
    <li><code>str</code> — строка: <code>"Привет"</code></li>
    <li><code>int</code> — целое число: <code>42</code></li>
    <li><code>float</code> — дробное число: <code>3.14</code></li>
    <li><code>bool</code> — логический тип: <code>True</code> или <code>False</code></li>
</ul>

<h3>Функция type()</h3>
<pre><code>x = 10
print(type(x))  # &lt;class 'int'&gt;</code></pre>

<h3>f-строки</h3>
<pre><code>name = "Мир"
print(f"Привет, {name}!")  # Привет, Мир!</code></pre>
                """,
                "questions": [
                    {
                        "question": "Какой тип данных у значения 3.14?",
                        "options": ["int", "str", "float", "bool"],
                        "answer": "float"
                    },
                    {
                        "question": "Какой тип данных у значения True?",
                        "options": ["int", "str", "float", "bool"],
                        "answer": "bool"
                    },
                    {
                        "question": "К какому типу данных относится число 5?",
                        "options": ["str", "int", "float", "bool"],
                        "answer": "int"
                    }
                ]
            },
            {
                "title": "Арифметические операции",
                "theory": """
<h3>Основные операторы</h3>
<table>
    <tr><td><code>+</code></td><td>Сложение</td><td><code>5 + 3 = 8</code></td></tr>
    <tr><td><code>-</code></td><td>Вычитание</td><td><code>5 - 3 = 2</code></td></tr>
    <tr><td><code>*</code></td><td>Умножение</td><td><code>5 * 3 = 15</code></td></tr>
    <tr><td><code>/</code></td><td>Деление</td><td><code>5 / 3 = 1.666...</code></td></tr>
    <tr><td><code>//</code></td><td>Целочисленное деление</td><td><code>5 // 3 = 1</code></td></tr>
    <tr><td><code>%</code></td><td>Остаток от деления</td><td><code>5 % 3 = 2</code></td></tr>
    <tr><td><code>**</code></td><td>Возведение в степень</td><td><code>5 ** 3 = 125</code></td></tr>
</table>

<h3>Приоритет операций</h3>
<pre><code>result = 2 + 3 * 4    # 14, а не 20
result = (2 + 3) * 4  # 20 — скобки меняют порядок</code></pre>

<h3>Преобразование типов</h3>
<pre><code>age_str = "25"
age_num = int(age_str)  # Строка в число
print(age_num + 5)       # 30</code></pre>
                """,
                "questions": [
                    {
                        "question": "Что вернёт 10 % 3?",
                        "options": ["3", "1", "0", "3.33"],
                        "answer": "1"
                    },
                    {
                        "question": "Что вернёт 2 ** 4?",
                        "options": ["8", "16", "6", "24"],
                        "answer": "16"
                    },
                    {
                        "question": "Что вернёт 7 // 2?",
                        "options": ["3.5", "3", "4", "2"],
                        "answer": "3"
                    }
                ]
            },
            {
                "title": "Условные операторы",
                "theory": """
<h3>Оператор if</h3>
<pre><code>age = 18
if age >= 18:
    print("Совершеннолетний")</code></pre>

<h3>if-else</h3>
<pre><code>temperature = 35
if temperature > 30:
    print("Жарко!")
else:
    print("Нормально")</code></pre>

<h3>if-elif-else</h3>
<pre><code>score = 85
if score >= 90:
    print("Отлично")
elif score >= 70:
    print("Хорошо")
elif score >= 50:
    print("Удовлетворительно")
else:
    print("Неудовлетворительно")</code></pre>

<h3>Логические операторы</h3>
<pre><code>x = 15
if x > 10 and x < 20:
    print("Между 10 и 20")

if x == 5 or x == 15:
    print("x равен 5 или 15")</code></pre>
                """,
                "questions": [
                    {
                        "question": "Что выведет: if 5 > 3: print('Да')?",
                        "options": ["Да", "Нет", "Ошибка", "Ничего"],
                        "answer": "Да"
                    },
                    {
                        "question": "Какой оператор означает И (оба условия истинны)?",
                        "options": ["or", "and", "not", "if"],
                        "answer": "and"
                    },
                    {
                        "question": "Что проверяет elif?",
                        "options": [
                            "Альтернативное условие",
                            "Конец программы",
                            "Цикл",
                            "Ошибку"
                        ],
                        "answer": "Альтернативное условие"
                    }
                ]
            },
            {
                "title": "Циклы for и while",
                "theory": """
<h3>Цикл for</h3>
<pre><code>for i in range(5):
    print(i)  # 0, 1, 2, 3, 4

for i in range(1, 6):
    print(i)  # 1, 2, 3, 4, 5</code></pre>

<h3>Перебор списка</h3>
<pre><code>fruits = ["яблоко", "банан", "вишня"]
for fruit in fruits:
    print(fruit)</code></pre>

<h3>Цикл while</h3>
<pre><code>count = 0
while count < 5:
    print(count)
    count += 1</code></pre>

<h3>break и continue</h3>
<pre><code>for i in range(10):
    if i == 5:
        break       # Остановить цикл
    if i % 2 == 0:
        continue    # Пропустить итерацию
    print(i)        # 1, 3</code></pre>
                """,
                "questions": [
                    {
                        "question": "Какие числа генерирует range(3)?",
                        "options": ["1, 2, 3", "0, 1, 2", "0, 1, 2, 3", "3"],
                        "answer": "0, 1, 2"
                    },
                    {
                        "question": "Что делает break?",
                        "options": [
                            "Останавливает цикл",
                            "Пропускает итерацию",
                            "Начинает цикл заново",
                            "Удаляет переменную"
                        ],
                        "answer": "Останавливает цикл"
                    },
                    {
                        "question": "Сколько раз выполнится: for i in range(1, 4)?",
                        "options": ["4", "3", "2", "1"],
                        "answer": "3"
                    }
                ]
            },
            {
                "title": "Списки (list)",
                "theory": """
<h3>Создание списка</h3>
<pre><code>numbers = [1, 2, 3, 4, 5]
mixed = [1, "hello", True, 3.14]
empty = []</code></pre>

<h3>Обращение к элементам</h3>
<pre><code>fruits = ["яблоко", "банан", "вишня"]
print(fruits[0])   # яблоко (индексация с 0!)
print(fruits[-1])  # вишня (с конца)</code></pre>

<h3>Методы списков</h3>
<pre><code>nums = [3, 1, 4]
nums.append(5)       # [3, 1, 4, 5]
nums.insert(0, 10)   # [10, 3, 1, 4, 5]
nums.remove(3)       # [10, 1, 4, 5]
nums.sort()          # [1, 4, 5, 10]
print(len(nums))     # 4</code></pre>

<h3>Срезы</h3>
<pre><code>nums = [0, 1, 2, 3, 4, 5]
print(nums[1:4])   # [1, 2, 3]
print(nums[:3])    # [0, 1, 2]
print(nums[3:])    # [3, 4, 5]</code></pre>
                """,
                "questions": [
                    {
                        "question": "Какой индекс у первого элемента списка?",
                        "options": ["1", "0", "-1", "first"],
                        "answer": "0"
                    },
                    {
                        "question": "Какой метод добавляет элемент в конец списка?",
                        "options": ["add", "push", "append", "insert"],
                        "answer": "append"
                    },
                    {
                        "question": "Что вернёт len([10, 20, 30])?",
                        "options": ["30", "3", "10", "60"],
                        "answer": "3"
                    }
                ]
            },
            {
                "title": "Функции",
                "theory": """
<h3>Создание функции</h3>
<pre><code>def greet(name):
    return f"Привет, {name}!"

message = greet("Алиса")
print(message)  # Привет, Алиса!</code></pre>

<h3>Параметры по умолчанию</h3>
<pre><code>def power(base, exp=2):
    return base ** exp

print(power(3))     # 9
print(power(3, 3))  # 27</code></pre>

<h3>Возврат нескольких значений</h3>
<pre><code>def min_max(numbers):
    return min(numbers), max(numbers)

lo, hi = min_max([3, 1, 7, 2])
print(lo, hi)  # 1 7</code></pre>

<h3>Функция без return</h3>
<pre><code>def say_hello():
    print("Привет!")
    # Возвращает None

result = say_hello()
print(result)  # None</code></pre>
                """,
                "questions": [
                    {
                        "question": "Каким ключевым словом объявляется функция?",
                        "options": ["func", "function", "def", "fn"],
                        "answer": "def"
                    },
                    {
                        "question": "Что делает return?",
                        "options": [
                            "Возвращает значение из функции",
                            "Печатает текст",
                            "Создаёт переменную",
                            "Завершает программу"
                        ],
                        "answer": "Возвращает значение из функции"
                    },
                    {
                        "question": "Что вернёт функция без return?",
                        "options": ["0", "Пустая строка", "None", "Ошибка"],
                        "answer": "None"
                    }
                ]
            },
            {
                "title": "Словари (dict)",
                "theory": """
<h3>Создание словаря</h3>
<pre><code>person = {
    "name": "Алиса",
    "age": 25,
    "city": "Москва"
}</code></pre>

<h3>Доступ к данным</h3>
<pre><code>print(person["name"])              # Алиса
print(person.get("phone", "Нет"))  # Нет</code></pre>

<h3>Изменение и добавление</h3>
<pre><code>person["age"] = 26             # Изменить
person["email"] = "a@b.com"    # Добавить
del person["city"]             # Удалить</code></pre>

<h3>Перебор словаря</h3>
<pre><code>for key, value in person.items():
    print(f"{key}: {value}")</code></pre>
                """,
                "questions": [
                    {
                        "question": "Из чего состоит элемент словаря?",
                        "options": [
                            "Ключ и значение",
                            "Индекс и значение",
                            "Имя и тип",
                            "Только значение"
                        ],
                        "answer": "Ключ и значение"
                    },
                    {
                        "question": "Что вернёт d.get('x', 0) если ключа x нет?",
                        "options": ["Ошибка", "None", "0", "x"],
                        "answer": "0"
                    },
                    {
                        "question": "Какой метод возвращает пары ключ-значение?",
                        "options": ["keys", "values", "items", "pairs"],
                        "answer": "items"
                    }
                ]
            },
            {
                "title": "Работа со строками",
                "theory": """
<h3>Методы строк</h3>
<pre><code>text = "Hello, World!"
print(text.upper())        # HELLO, WORLD!
print(text.lower())        # hello, world!
print(text.replace("World", "Python"))  # Hello, Python!
print(text.split(", "))    # ['Hello', 'World!']
print(len(text))           # 13</code></pre>

<h3>f-строки</h3>
<pre><code>name = "Алиса"
age = 25
print(f"Имя: {name}, возраст: {age}")
print(f"Через 5 лет: {age + 5}")</code></pre>

<h3>Проверки строк</h3>
<pre><code>"hello".startswith("he")   # True
"hello".endswith("lo")     # True
"123".isdigit()            # True
"  hi  ".strip()           # "hi"</code></pre>
                """,
                "questions": [
                    {
                        "question": "Какой метод переводит строку в верхний регистр?",
                        "options": ["upper", "capitalize", "big", "top"],
                        "answer": "upper"
                    },
                    {
                        "question": "Что делает метод split?",
                        "options": [
                            "Разделяет строку на список",
                            "Объединяет строки",
                            "Удаляет пробелы",
                            "Заменяет символы"
                        ],
                        "answer": "Разделяет строку на список"
                    },
                    {
                        "question": "Что вернёт '123'.isdigit()?",
                        "options": ["True", "False", "123", "Ошибка"],
                        "answer": "True"
                    }
                ]
            },
            {
                "title": "Основы ООП — Классы",
                "theory": """
<h3>Создание класса</h3>
<pre><code>class Dog:
    def __init__(self, name, breed):
        self.name = name
        self.breed = breed

    def bark(self):
        return f"{self.name} говорит: Гав!"</code></pre>

<h3>Создание объектов</h3>
<pre><code>my_dog = Dog("Бобик", "Лабрадор")
print(my_dog.bark())   # Бобик говорит: Гав!
print(my_dog.name)     # Бобик</code></pre>

<h3>Наследование</h3>
<pre><code>class Puppy(Dog):
    def __init__(self, name, breed, toy):
        super().__init__(name, breed)
        self.toy = toy

    def play(self):
        return f"{self.name} играет с {self.toy}"

p = Puppy("Шарик", "Корги", "мячиком")
print(p.bark())   # Шарик говорит: Гав!
print(p.play())   # Шарик играет с мячиком</code></pre>

<p>🎉 <strong>Поздравляем! Вы прошли основы Python!</strong></p>
                """,
                "questions": [
                    {
                        "question": "Каким ключевым словом создаётся класс?",
                        "options": ["def", "class", "object", "new"],
                        "answer": "class"
                    },
                    {
                        "question": "Как называется метод-конструктор в Python?",
                        "options": ["__init__", "__new__", "constructor", "create"],
                        "answer": "__init__"
                    },
                    {
                        "question": "Что означает self в методах класса?",
                        "options": [
                            "Ссылка на текущий объект",
                            "Имя класса",
                            "Глобальная переменная",
                            "Тип данных"
                        ],
                        "answer": "Ссылка на текущий объект"
                    }
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
<h3>Что такое JavaScript?</h3>
<p>JavaScript — язык, который делает веб-страницы интерактивными.</p>

<h3>Вывод в консоль</h3>
<pre><code>console.log("Привет, мир!");</code></pre>

<h3>Переменные</h3>
<pre><code>let name = "JavaScript";    // Можно изменять
const PI = 3.14;             // Нельзя изменять</code></pre>

<h3>Типы данных</h3>
<pre><code>let str = "Hello";       // String
let num = 42;            // Number
let flag = true;         // Boolean
let empty = null;        // Null
let x;                   // Undefined</code></pre>
                """,
                "questions": [
                    {
                        "question": "Какая функция выводит в консоль в JavaScript?",
                        "options": ["print", "console.log", "echo", "write"],
                        "answer": "console.log"
                    },
                    {
                        "question": "Какое ключевое слово создаёт неизменяемую переменную?",
                        "options": ["let", "var", "const", "static"],
                        "answer": "const"
                    },
                    {
                        "question": "Какой тип у неинициализированной переменной (let x;)?",
                        "options": ["null", "undefined", "string", "number"],
                        "answer": "undefined"
                    }
                ]
            },
            {
                "title": "Условия и циклы",
                "theory": """
<h3>if / else</h3>
<pre><code>let age = 20;
if (age >= 18) {
    console.log("Совершеннолетний");
} else {
    console.log("Несовершеннолетний");
}</code></pre>

<h3>Строгое сравнение</h3>
<pre><code>5 == "5"   // true  (нестрогое)
5 === "5"  // false (строгое — проверяет тип!)
// Всегда используйте ===</code></pre>

<h3>Цикл for</h3>
<pre><code>for (let i = 0; i < 5; i++) {
    console.log(i);
}</code></pre>

<h3>Цикл while</h3>
<pre><code>let count = 0;
while (count < 5) {
    console.log(count);
    count++;
}</code></pre>
                """,
                "questions": [
                    {
                        "question": "Что вернёт 5 === '5'?",
                        "options": ["true", "false", "5", "Ошибка"],
                        "answer": "false"
                    },
                    {
                        "question": "Что означает i++ в цикле for?",
                        "options": ["i = i + 1", "i = i - 1", "i = i * 2", "i = 0"],
                        "answer": "i = i + 1"
                    },
                    {
                        "question": "Какие скобки используются для блока кода в JS?",
                        "options": ["Круглые ()", "Квадратные []", "Фигурные {}", "Угловые <>"],
                        "answer": "Фигурные {}"
                    }
                ]
            },
            {
                "title": "Функции",
                "theory": """
<h3>Объявление функции</h3>
<pre><code>function greet(name) {
    return "Привет, " + name + "!";
}
console.log(greet("Мир"));</code></pre>

<h3>Стрелочные функции</h3>
<pre><code>const double = (x) => x * 2;
console.log(double(5));  // 10

const add = (a, b) => {
    return a + b;
};</code></pre>

<h3>Параметры по умолчанию</h3>
<pre><code>function power(base, exp = 2) {
    return base ** exp;
}
console.log(power(3));     // 9
console.log(power(3, 3));  // 27</code></pre>
                """,
                "questions": [
                    {
                        "question": "Каким словом объявляется функция в JS?",
                        "options": ["def", "func", "function", "fn"],
                        "answer": "function"
                    },
                    {
                        "question": "Как записывается стрелочная функция?",
                        "options": [
                            "() => {}",
                            "() -> {}",
                            "() >> {}",
                            "() ~> {}"
                        ],
                        "answer": "() => {}"
                    },
                    {
                        "question": "Что вернёт функция без return?",
                        "options": ["0", "null", "undefined", "Ошибка"],
                        "answer": "undefined"
                    }
                ]
            },
            {
                "title": "Массивы",
                "theory": """
<h3>Создание и доступ</h3>
<pre><code>let fruits = ["яблоко", "банан", "вишня"];
console.log(fruits[0]);     // яблоко
console.log(fruits.length); // 3</code></pre>

<h3>Методы массивов</h3>
<pre><code>let arr = [1, 2, 3];
arr.push(4);           // [1, 2, 3, 4]
arr.pop();             // [1, 2, 3]
arr.includes(2);       // true</code></pre>

<h3>map, filter, reduce</h3>
<pre><code>let nums = [1, 2, 3, 4, 5];

let doubled = nums.map(x => x * 2);
// [2, 4, 6, 8, 10]

let evens = nums.filter(x => x % 2 === 0);
// [2, 4]

let sum = nums.reduce((acc, x) => acc + x, 0);
// 15</code></pre>
                """,
                "questions": [
                    {
                        "question": "Какой метод добавляет элемент в конец массива?",
                        "options": ["add", "append", "push", "insert"],
                        "answer": "push"
                    },
                    {
                        "question": "Что делает метод filter?",
                        "options": [
                            "Фильтрует элементы по условию",
                            "Сортирует массив",
                            "Удаляет дубликаты",
                            "Переворачивает массив"
                        ],
                        "answer": "Фильтрует элементы по условию"
                    },
                    {
                        "question": "Что вернёт [1, 2, 3].length?",
                        "options": ["3", "2", "Массив", "Ошибка"],
                        "answer": "3"
                    }
                ]
            }
        ]
    },
    "html_css": {
        "id": "html_css",
        "title": "HTML & CSS",
        "icon": "🎨",
        "color": "#E44D26",
        "description": "Создавайте красивые веб-страницы",
        "lessons": [
            {
                "title": "Структура HTML",
                "theory": """
<h3>Что такое HTML?</h3>
<p>HTML — язык разметки для создания веб-страниц.</p>

<h3>Базовая структура</h3>
<pre><code>&lt;!DOCTYPE html&gt;
&lt;html&gt;
&lt;head&gt;
    &lt;title&gt;Моя страница&lt;/title&gt;
&lt;/head&gt;
&lt;body&gt;
    &lt;h1&gt;Привет!&lt;/h1&gt;
    &lt;p&gt;Это параграф.&lt;/p&gt;
&lt;/body&gt;
&lt;/html&gt;</code></pre>

<h3>Основные теги</h3>
<ul>
    <li><code>&lt;h1&gt;...&lt;h6&gt;</code> — заголовки</li>
    <li><code>&lt;p&gt;</code> — параграф</li>
    <li><code>&lt;a href="..."&gt;</code> — ссылка</li>
    <li><code>&lt;img src="..."&gt;</code> — изображение</li>
    <li><code>&lt;ul&gt;, &lt;ol&gt;, &lt;li&gt;</code> — списки</li>
    <li><code>&lt;div&gt;</code> — блок</li>
</ul>
                """,
                "questions": [
                    {
                        "question": "Какой тег является главным заголовком страницы?",
                        "options": ["title", "h1", "header", "head"],
                        "answer": "h1"
                    },
                    {
                        "question": "Где размещается видимое содержимое страницы?",
                        "options": ["head", "body", "html", "meta"],
                        "answer": "body"
                    },
                    {
                        "question": "Какой тег создаёт ссылку?",
                        "options": ["link", "a", "href", "url"],
                        "answer": "a"
                    }
                ]
            },
            {
                "title": "Основы CSS",
                "theory": """
<h3>Что такое CSS?</h3>
<p>CSS — язык стилей для оформления HTML.</p>

<h3>Синтаксис</h3>
<pre><code>h1 {
    color: blue;
    font-size: 24px;
    text-align: center;
}

.my-class {
    background-color: #f0f0f0;
    padding: 20px;
    border-radius: 10px;
}</code></pre>

<h3>Селекторы</h3>
<ul>
    <li><code>h1</code> — по тегу</li>
    <li><code>.class</code> — по классу</li>
    <li><code>#id</code> — по идентификатору</li>
</ul>

<h3>Box Model</h3>
<pre><code>.box {
    width: 200px;
    padding: 20px;       /* Внутренний отступ */
    border: 2px solid;   /* Граница */
    margin: 10px;        /* Внешний отступ */
}</code></pre>
                """,
                "questions": [
                    {
                        "question": "Какое свойство задаёт цвет текста?",
                        "options": ["font-color", "text-color", "color", "background"],
                        "answer": "color"
                    },
                    {
                        "question": "Какой символ обозначает класс в CSS?",
                        "options": ["#", ".", "@", "&"],
                        "answer": "."
                    },
                    {
                        "question": "Какое свойство задаёт внутренний отступ?",
                        "options": ["margin", "padding", "border", "spacing"],
                        "answer": "padding"
                    }
                ]
            },
            {
                "title": "Flexbox",
                "theory": """
<h3>Что такое Flexbox?</h3>
<p>Мощный способ выравнивания элементов.</p>

<pre><code>.container {
    display: flex;
    justify-content: center;   /* По горизонтали */
    align-items: center;       /* По вертикали */
    gap: 10px;
}</code></pre>

<h3>justify-content</h3>
<ul>
    <li><code>flex-start</code> — в начале</li>
    <li><code>center</code> — по центру</li>
    <li><code>space-between</code> — равные промежутки</li>
</ul>

<h3>flex-direction</h3>
<pre><code>.container {
    flex-direction: row;      /* Горизонтально */
    flex-direction: column;   /* Вертикально */
}</code></pre>
                """,
                "questions": [
                    {
                        "question": "Какое значение display включает Flexbox?",
                        "options": ["block", "inline", "flex", "grid"],
                        "answer": "flex"
                    },
                    {
                        "question": "Какое свойство выравнивает по горизонтали?",
                        "options": ["align-items", "justify-content", "flex-direction", "gap"],
                        "answer": "justify-content"
                    },
                    {
                        "question": "Какое значение flex-direction располагает элементы вертикально?",
                        "options": ["row", "column", "vertical", "block"],
                        "answer": "column"
                    }
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