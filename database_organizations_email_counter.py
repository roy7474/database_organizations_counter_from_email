import sqlite3

conn = sqlite3.connect('organizations_from_emails_in_mbox_file.sqlite')
cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS Counts')

cur.execute('''
CREATE TABLE Counts (organization TEXT, count INTEGER)''')

fname = input('Enter file name: ')
if (len(fname) < 1): fname = 'mbox.txt'
fh = open(fname)
for line in fh:
    if not line.startswith('From: '): continue
    pieces = line.split()
    email = pieces[1]
    emailParts = email.split('@')
    organization = emailParts[-1]

    cur.execute('SELECT count FROM Counts WHERE organization = ? ', (organization, ))
    row = cur.fetchone()
    if row is None:
        cur.execute('''INSERT INTO Counts (organization, count)
                VALUES (?, 1)''', (organization, ))
    else:
        cur.execute('UPDATE Counts SET count = count + 1 WHERE organization = ?',
                    (organization, ))
    conn.commit()

# https://www.sqlite.org/lang_select.html
sqlstr = 'SELECT organization, count FROM Counts ORDER BY count DESC'

for row in cur.execute(sqlstr):
    print(str(row[0]), row[1])
print('Counts:')
cur.close()