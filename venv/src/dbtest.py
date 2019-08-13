import mysql.connector
import json, collections
import tablib
from pdfdocument.document import PDFDocument


def toPdf(path, text):

    pdf = PDFDocument(path)
    pdf.init_report()
    pdf.p(text)
    pdf.generate()

def toJsonFile(path, jsonData):
    file = open(path,'w')
    json.dump(jsonData, file)
    file.close()
    print(path+"created")


def jsonTOExcel(content,export_fileName):
    headers = mycursor.column_names
    tb = tablib.Dataset(*content, headers=headers)
    try:
        with open(export_fileName, 'wb') as f:
            f.write(tb.export('xls'))
        f.close()
    except BaseException as e:
        print(e)



db = mysql.connector.connect(
    host='localhost',
    user='root',
    password='root',
    database='pythondbtest'
)
mycursor = db.cursor()

sqlAddCol = 'alter table employees add _______'
sqlDel = 'delete from employees where name=%s'
sqlAddData = 'insert into employees (name,age) values (%s,%s)'
sqlShow = 'select name,age from employees'
placeholer = ('jai',)

mycursor.execute(sqlDel, placeholer)
#db.commit()
data = mycursor.fetchall()
#print(data)
col = mycursor.column_names

# convert row data to json  
'''list = []
for row in data:
    list.append(dict(zip(col, row)))
jsonData = json.dumps(list)'''


#jsonTOExcel(data, 'rowToExcel.xls')

#toJsonFile("test.json",jsonData)





