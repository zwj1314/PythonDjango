import sqlite3

conn = sqlite3.connect('test.db')
create_sql = 'CREATE TABLE company(id INT PRIMARY KEY NOT NULL, emp_name text NOT NULL);'
conn.execute(create_sql)
insert_sql = 'INSERT INTO company VALUES (?, ?)'
conn.execute(insert_sql, (100, 'LY'))
conn.execute(insert_sql, (200, 'July'))
cursors = conn.execute('SELECT id, emp_name FROM company')
for row in cursors:
    print(row[0], row[1])
conn.close()
