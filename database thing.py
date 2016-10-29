import sqlite3

conn = sqlite3.connect("database.db")
cur = conn.cursor()
incr = ["", "13068481", "13", "10/03/2015", "03/03/2015"]
loanNO = 7


for i in range(0, 500):
    incr = list(incr)
    SQL = "INSERT INTO Loan(loanNo, studID, bookCopyNo, returnDate, borrowDate) "
    SQL = SQL + "VALUES(?,?,?,?,?)"
    incr[0] = str(loanNO)
    loanNO = loanNO + 1
    incr = tuple(incr)
    cur.execute(SQL, incr)
    conn.commit()

