import socket
import threading
import time
import json
import os
from os.path import exists

#Account acces class
def addAccount(login, password):
    data={
        'login': login,
        'password': password
    }
    fl=open('accounts.json', 'r')
    rec=json.load(fl)
    rec['acs'].append(data)
    fl.close()

    fl=open('accounts.json', 'w')
    json.dump(rec, fl)
    fl.close()
    return 1
def isAccountExist(login):
    with open('accounts.json', 'r') as fl:
        rec=json.load(fl)
        fl.close()
        for i in range(len(rec['acs'])):
            if rec['acs'][i]['login'] == login:
                return 1
        return 0
def getAccount(login):
    with open('accounts.json', 'r') as fl:
        rec = json.load(fl)
        fl.close()
        for i in range(len(rec['acs'])):
            if rec['acs'][i]['login'] == login:
                return rec['acs'][i]
        return 0

######################################################
######################################################
######################################################

if not exists('files'):
    os.mkdir('files')

if not exists('accounts.json'):
    ir=open('accounts.json', 'w')
    lo={
        'acs': []
    }
    json.dump(lo, ir)
    ir.close()

#settings
if not exists('settings.json'):
    with open('settings.json', 'w') as lov:
        default={
            'password': '1023',
            'port': 23401
        }
        json.dump(default, lov)
        lov.close()

print('Protected chat server v1.0 by Sirtage.')

with open('settings.json', 'r') as re:
    settings=json.load(re)
    password = settings['password']
    PORT = settings['port']
    re.close()

#livetime connection class
class connector:
    def __init__(self, name, conn):
        self.name = name
        self.connection = conn

def containsName(nm):
    for i in range(len(connected)):
        if connected[i].name==nm:
            return 1
    return 0

connected=[]

s = socket.socket()
s.bind(('', PORT))
s.listen()

#Send message to all users
def sendToAll(msg):
    temp=[]
    for i in range(len(connected)):
        try:
            connected[i].connection.send(b'71')
            connected[i].connection.send(str(msg).encode())
        except:
            temp.append(connected[i])
    print(msg)
    for i in range(len(temp)):
        try:
            temp[i].close()
        except:
            1
        connected.remove(temp[i])

#User permission updator
def user(username, cn):
    while True:
        try:
            dt = cn.recv(1024)
            dt=dt.decode()
            #message
            if dt == '1011':
                msg = cn.recv(1024)
                sendToAll(username+">"+msg.decode())
            elif dt == '2421':
                retr='Channel members: '
                for i in range(len(connected)):
                    retr+='\n'+connected[i].name
                cn.send(b'71')
                cn.send(retr.encode())
            elif dt == '-901':
                for i in range(len(connected)):
                    if connected[i].name==username:
                        connected.remove(connected[i])
                        sendToAll(f'{username} disconnected.')
                        break
            elif dt == '96':
                nkm=cn.recv(1024)
                file=cn.recv(1000000000)
                nw = open('files/'+nkm.decode(), 'wb')
                nw.write(file)
                nw.close()
            elif dt == '104':
                stk='Files: '
                ls=os.listdir('files')
                for i in range(len(ls)):
                    stk+='\n'+ls[i]+' | '+str(os.stat('files/'+ls[i]).st_size)
                cn.send(b'72')
                cn.send(stk.encode())
                ilk=cn.recv(1024)
                if ilk.decode()=='1':
                    cn.send(b'1')
                else:
                    continue
            elif dt == '81':
                cn.send(b'456')
                ftdname=cn.recv(1024)
                if exists('files/'+ftdname.decode()):
                    cn.send(ftdname)
                    cn.recv(1024)
                    cn.send(open('files/'+ftdname.decode(), 'rb').read())
                else:
                    cn.send(b'-1')
            #not known format
            else:
                cn.send(b'0')
        except:
            print(f'Error with {username}({cn})')
            break

#adding user
def addUser(cnlp):
    try:
        pswd=cnlp.recv(1024)
        if pswd.decode()==password:
            cnlp.send(b'True')
            while True:
                _login = cnlp.recv(1024)
                if isAccountExist(_login.decode()):
                    cnlp.send(b'l')
                    pswd = cnlp.recv(1024)
                    if pswd.decode()==getAccount(_login.decode())['password']:
                        cnlp.send(b'111011')
                        connected.append(connector(_login.decode(), cnlp))
                        a = threading.Thread(target=user, args=(_login.decode(), cnlp,))
                        a.start()
                        sendToAll(f'{_login.decode()} connected.')
                        break
                    else:
                        cnlp.send(b'90012')
                else:
                    cnlp.send(b'r')
                    new_pswd=cnlp.recv(1024)
                    if new_pswd.decode()!='-c':
                        try:
                            addAccount(_login.decode(), new_pswd.decode())
                            cnlp.send(b'y')
                            continue
                        except:
                            cnlp.send(b'Es')
                            continue
                    elif new_pswd.decode()=='-c':
                        continue
                    else:
                        cnlp.send(b'n')
                        continue
        else:
            cnlp.send(b'False')
            cnlp.close()
    except:
        print(f'{cnlp} cancelled connect or something went wrong.')
        cnlp.close()

#connection receiver
def run():
    print('Started.')
    while True:
        conn, addr = s.accept()
        frun=threading.Thread(target=addUser, args=(conn,))
        frun.start()
run()