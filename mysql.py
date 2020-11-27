from imp import cursor, connection

#cursor.execute('create database telegram_bot')
#connection.commit()

cursor.execute('CREATE TABLE const_info(id INT AUTO_INCREMENT PRIMARY KEY, data TEXT)')
connection.commit()

cursor.execute('CREATE TABLE reviews(id INT AUTO_INCREMENT PRIMARY KEY, data TEXT)')
connection.commit()

cursor.execute("INSERT INTO const_info VALUES (%s, %s)", (1, 't.me/heree_name'))
connection.commit()

cursor.execute("INSERT INTO const_info VALUES (%s, %s)", (2, 'yandex.ru'))
connection.commit()

cursor.execute("INSERT INTO const_info VALUES (%s, %s)", (3, 'fgsdfg@yandex.ru'))
connection.commit()

cursor.execute("INSERT INTO const_info VALUES (%s, %s)", (4, 'все'))
connection.commit()

cursor.execute("INSERT INTO const_info VALUES (%s, %s)", (5, 'fgdfgdfgdfg'))
connection.commit()

cursor.execute("INSERT INTO reviews VALUES (%s, %s)", (1, 'супер'))
connection.commit()