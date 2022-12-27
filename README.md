Этот проект - реализация REST API приложения на микрофреймворке Flask.<br>
Позволяет добавлять, получать и удалять определенные редакции книг.<br>


<b>Используемые библиотеки:</b>
<ul>
<li>Flask-SQLAlchemy - для взаимодействия с базой данных;</li>
<li>Flask-Migrate - для управления миграциями БД;</li>
<li>Flask-JWT-extended - для поддержки JWT-токенов.</li>
</ul>
<b>Структура проекта:</b><br>

        .<br>
        ├── app<br>
        │   ├──api<br>
        │   │   ├── __init__.py<br>
        │   │   ├── responses.py<br>
        │   │   ├── routes.py<br>
        │   │   ├── user.py<br>
        │   │   └── validators.py<br>
        │   ├── tests<br>
        │   ├── __init__.py<br>
        │   └──  models.py<br>
        ├── migrations<br>
        ├── config.py<br>
        ├── main.py<br>
        └── requirements.txt<br>
        
app - каталог с файлами приложения:<br>
     api/routes.py и api/users.py - маршруты;<br>
     api/responses.py и api/validators.py - вспомогательные модули;<br>
     tests - модульные тесты<br>
migrations - сценарии миграций<br>
config.py - файл конфигурации<br>
main.py - точка входа<br>

<b>Запуск приложения:</b><br>

<ol>
<li>Клонировать репозиторий</li>
<li>Установить виртуальную среду и библиотеки (pip install requirements.txt)</li>
<li>Установить значения глобальных переменных (файл конфигурации импортирует значения глобальных переменных из файла .env, при их отсутствии устанавливает значения по умолчанию):<br>
  SECRET_KEY, JWT_KEY, DATABASE_URL</li>
<li>В терминале или в файле .flaskenv установить FLASK_APP=main</li>
<li>Создать базу данных:

      flask db init<br>
      flask db migrate<br>
      flask db upgrade
    
   Для тестов используется база данных SQLite.</li>

<li>Запустить сервер:

    flask run
    
</li><br>


<b>База данных</b><br>
Содержит следующие модели:
<ul type="disc">
<li>User - зарегистрированные пользователи (поля: id (pk), username, email, password_hash)</li>
<li>Book - оригинальные названия книг (поля: id (pk), title)</li>
<li>Author - имена авторов (в т.ч. переводчиков, иллюстраторов и т.д.) (поля: id (pk), name)</li>
<li>Role - роли авторов при издании книг (поля: id (pk), name)</li>
<li>Publisher - издательства (поля: id (pk), name)</li>
<li>Language - языки изданий (поля: id (pk), name)</li>
<li>Edition - конкретные издания книг (поля: id (pk), isbn (unique), book_id, publisher_id, language_id, year, text)</li>
<li>EditionAuthor - устанавливает отношения многие-ко-многим с авторами и их ролями (поля: id (pk), edition_id, author_id, role_id, order)</li>
</ul>
Графическое представление моделей и их взаимосвязей:<br>

<img width="494" alt="db_books" src="https://user-images.githubusercontent.com/109738460/206855909-e1159a2e-262d-4e49-84c8-ee58ec13d2ac.PNG">

<br>
<br>
<b>Поддерживаемые методы API</b><br>
<ol type="1">
  <li>Регистрация пользователя<br>
    Запрос:

      POST http://127.0.0.1:5000/api/register
      {
      "username": "john doe",
      "email": "john@example.com",
      "password": "psw123"
      }
  
   Ответ:
   
      201 
      {
      "message": "<User john doe> was created"
      }
     
  </li>
  <li>Авторизация, запрос токена<br>
    Запрос:
    
      POST http://127.0.0.1:5000/api/login
      {
      "username": "john doe",
      "password": "pswd123"
      }
      
   Ответ:  
   
      200 
      {
      "message": "Logged in as john doe",
      "access_token": access_token,
      "refresh_token": refresh_token
      }
       
  </li>
  <li>Рефреш токена<br>
     Запрос:
     
      GET http://127.0.0.1:5000/api/token/refresh
      HEADERS:
      Authorization: refresh_token
      
   Ответ:  
    
      200 
      {
      "access_token": access_token
      }
      
  </li>
 Приложение поддерживает CRUD-операции всех таблиц БД (кроме User) посредством POST, GET, PUT и DELETE-запросов.
 Маршрут для POST-запросов: 
    
      http://127.0.0.1:5000/api/<имя таблицы>
 Маршрут для GET, PUT и DELETE-запросов: 
    
      http://127.0.0.1:5000/api/<имя таблицы>/<int:id>   
 
 POST и PUT запросы требуют передачи JSON-формата с ключами - именами полей таблицы. 

 Для запросов необходима передача токена доступа в заголовках:<br>
 HEADERS:<br>
  Authorization: access_token<br>
  
Примеры запросов к таблице Edition:
  <li>Получение редакции книги по id редакции<br>
    Запрос:
    
      GET http://127.0.0.1:5000/api/edition/<int:id>
      
   Ответ:  
    
      200 
None, 'text': None, 'edition_author': []}

      {
      "id": "",
      "isbn": "",
      "book_id": "",
      "book": "",
      "publisher_id": "",
      "publisher": "",
      "language_id": "",
      "language": "",
      "year": "",
      "text": "",
      "edition_author": []
      }

  </li>
  <li>Добавление редакции книги в БД<br>
    Запрос:
    
      POST http://127.0.0.1:5000/api/edition
      {
      "book_id": "",
      "isbn": "",
      "language_id": "",
      "publisher_id": "",
      "text": ""
      }
      
   Ответ:  
  
      201 
      {
      }
   
  </li>
  <li>Изменение редакции книги по id<br>
    Запрос:
    
      POST http://127.0.0.1:5000/api/edition/<int:id>
      {
      <поля, которые требуется изменить, аналогично запросу на добавление>
      }
      
   Ответ:  
    
      204 
      {
      }   
   
  </li>
  <li>Удаление редакции книги по id<br>
    Запрос:
    
      DELETE http://127.0.0.1:5000/api/edition/<int:id>
    
   Ответ:  
   
      204 
      {
      }   
      
  </li>
</ol>
   
   
   
 
 
 
