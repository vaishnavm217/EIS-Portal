import sqlite3
from datetime import datetime
db= sqlite3.connect('/home/vaishnavm/web2py/applications/eisenergy/databases/storage.sqlite')
curs=db.cursor()
while True:
    first=last=datetime.now()
    x=curs.execute('SELECT * FROM instap')
    y=x.fetchall()
    count=0
    sum_power=0.0
    #print len(y)
    for i in y:
        sum_power+=i[2]
        if count==0 :
            first=datetime.strptime(i[1],"%Y-%m-%d %H:%M:%S")
            count+=1
        elif count==len(y)-1:
            last=datetime.strptime(i[1],"%Y-%m-%d %H:%M:%S")
        count+=1
    diff=last-first
    if diff.days>0 and len(y)>0:
        print "deletion starts"
        avg=sum_power/float(len(y))
        curs.execute('INSERT INTO dailyp(timestamp,power) values ("'+last.strftime('%Y-%m-%d %H:%M:%S')+'",'+str(avg)+')')
        db.commit()
        curs.execute('DELETE FROM instap')
        db.commit()