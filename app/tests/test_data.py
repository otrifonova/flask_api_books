class TestData:
    username = "john doe"
    email = "john@example.com"
    psw = "psw123"

    test_user_register = {"username": username,
                          "email": email,
                          "password": psw}
    test_user_login = {"username": username,
                       "password": psw}

    book_1 = {"title": "Анна Каренина"}
    language_1 = {"name": "русский"}
    language_2 = {"name": "английский"}
    publisher_1 = {"name": "АСТ"}
    publisher_2 = {"name": "CreateSpace Independent Publishing Platform"}
    author_1 = {"name": "Толстой Лев Николаевич"}
    author_2 = {"name": "Констанция Гарнетт"}
    role_1 = {"name": "автор"}
    role_2 = {"name": "переводчик"}
    edition_1 = {"book_id": 1,
                 "isbn": "9785170878888",
                 "language_id": 1,
                 "publisher_id": 1,
                 "text": "Все счастливые семьи похожи друг на друга, "
                         "каждая несчастливая семья несчастлива по-своему.",
                 "year": 2022}
    edition_2 = {"isbn": "9781482653755",
                 "book_id": 1,
                 "publisher_id": 2,
                 "language_id": 2,
                 "year": 2013,
                 "text": "Happy families are all alike; "
                         "every unhappy family is unhappy in its own way."}
    edition_author_1 = {"author_id": 1,
                        "edition_id": 1,
                        "order": 1,
                        "role_id": 1}
    edition_author_2 = {"edition_id": 2,
                        "author_id": 1,
                        "role_id": 1,
                        "order": 1}
    edition_author_3 = {"edition_id": 2,
                        "author_id": 2,
                        "role_id": 2,
                        "order": 2}

    book_1_updated = {"title": "Anna Karenina"}
    language_1_updated = {"name": "russian"}
    publisher_1_updated = {"name": "AST"}
    author_1_updated = {"name": "Leo Tolstoy"}
    role_1_updated = {"name": "writer"}
    edition_1_updated = {"isbn": "9785170878888",
                         "book_id": 1,
                         "publisher_id": 1,
                         "language_id": 1,
                         "year": 2022,
                         "text": "test test test test test"}
    edition_author_1_updated = {"edition_id": 1,
                                "author_id": 1,
                                "role_id": 1,
                                "order": 0}
