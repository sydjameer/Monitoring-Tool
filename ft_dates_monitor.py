# Developed by: Syed Jameer
# Date:06-Jun-2018
# Purpose: To fetch tp_application dates from different backend application

# ALL IMPORTS
from tkinter import *
import ibm_db
import datetime
from datetime import date
import configparser

#ALL CLASSES
class Connection:

    def __init__(self,dbname,hostname,port,uid,pwd,schema):
        self.dbname=dbname
        self.hostname=hostname
        self.port=port
        self.uid=uid
        self.pwd=pwd
        self.schema=schema

    def dates(self):
        try:
            conn_string='DATABASE={};HOSTNAME={};PORT={};PROTOCOL=TCPIP;UID={};PWD={}'.format(self.dbname,self.hostname,self.port,self.uid,self.pwd)
            query = 'select processing_date,eod_processing_date,next_processing_date from {}.TP_APPLICATION'.format(self.schema)
            connection = ibm_db.connect(conn_string,"","")
            stmt = ibm_db.exec_immediate(connection,query)
            tuple = ibm_db.fetch_tuple(stmt)
            ibm_db.close(connection)
            return (tuple)
        except:
            tuple=('Conn Err','Conn Err','Conn Err')
            return(tuple)

def configure(appname):
    config = configparser.ConfigParser()
    config.read('db_monitor.ini')
    conf_tuple = (config[appname]['database_name'], config[appname]['ip_address'], config[appname]['port_no'],
    config[appname]['username'], config[appname]['password'], config[appname]['schema'])
    return conf_tuple

# ALL DATABASE OBJECTS

today = date.today()
before= today+datetime.timedelta(days=-1)
after= today+datetime.timedelta(days=1)

#**********GUI Layuout**************
root=Tk()
root.title('Database date monitor')
root.iconbitmap('monitor_PJ5_icon.ico')
root.geometry('600x300')

field=Label(root,relief=SUNKEN,text='Application',width=15)
field.grid(row=0,column=3)
field=Label(root,relief=SUNKEN,text='Processing Date',bg='yellow',width=20)
field.grid(row=0,column=4)
field=Label(root,relief=SUNKEN,text='EOD Processing date',bg='yellow',width=20)
field.grid(row=0,column=5)
field=Label(root,relief=SUNKEN,text='Next Processing date',bg='yellow',width=20)
field.grid(row=0,column=6)

config = configparser.ConfigParser()
config.read('db_monitor.ini')
myapplist=config.sections()
print('Loading application info!..............')

i=1
for apps in myapplist:
    print('Fetching dates for '+apps)
    # To print application names
    field4 = Label(root, relief=RIDGE, text=apps, width=15)
    field4.grid(row=i, column=3)

    fetch=configure(apps)
    conn_object=Connection(fetch[0],fetch[1],fetch[2],fetch[3],fetch[4],fetch[5])  # Create object using Connection Class
    myobj=conn_object.dates()                # Gets the dates using dates method in Connection Class

    # To print application dates
    # index 0 is Current Processing date
    field1 = Label(root, relief=RIDGE,text=myobj[0],fg='Red' if myobj[0]!=today else 'Black',width=20)
    field1.grid(row=i, column=4)
    # index 1 is EOD processing date
    field1 = Label(root, relief=RIDGE,text=myobj[1],fg='Red' if myobj[1]!=before else 'Black',width=20)
    field1.grid(row=i, column=5)
    # index 2 is Next processing date
    field1 = Label(root, relief=RIDGE,text=myobj[2],fg='Red' if myobj[2]!=after else 'Black',width=20)
    field1.grid(row=i, column=6)
    i+=1

root.mainloop()

