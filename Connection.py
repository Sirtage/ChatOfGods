import socket
import threading
import os
import time
from os.path import exists

name=''
HOST=''
PORT=0
op72=0
data=''
filename=''

if not exists('downloads'):
    os.mkdir('downloads')

def close():
    input('[Press any button]')
    exit()

def process(code):
    if code=='2':
        1

def recieve():
    global op72
    global filename
    while True:
        if 1:
            code = s.recv(1024)
            #get message
            if code.decode()=='71':
                msg = s.recv(1024)
                print(msg.decode())
            #get something with given size
            elif code.decode()=='72':
                data=s.recv(1000000)
                s.send(b'1')
                pub=s.recv(64)
                if pub.decode()=='1':
                    print(data.decode())
                else:
                    process(pub)
            elif code.decode()=='456':
                send(filename)
                fname=s.recv(1024)
                if fname.decode()=='-1':
                    print('File does not exists.')
                else:
                    s.send(b'1')
                    data=s.recv(1000000000)
                    nw=open('downloads/'+fname.decode(), 'wb')
                    nw.write(data)
                    nw.close()
                op72=0


        #except:
        #    print('Server closed.')
        #    break

def send(something):
    s.send(something.encode())

def sendMsg(msg):
    send('1011')
    send(msg)

def sendFile(path):
    mode='a'
    f=open(path, 'rb')
    if mode=='a':
        send('96')
        stk=''
        fname=f.name
        for i in range(len(fname)):
            if fname[i]=='/':
                stk=''
                continue
            stk+=fname[i]
        send(stk)
        time.sleep(0.1)
        s.send(f.read())
    elif mode=='b':
        send('97')

def downloadFile(fname):
    global filename
    filename=fname
    send('81')

def gcv():
    global op72
    while True:
        if op72: continue
        message = str(input())
        if len(message)==0: continue
        if message[0]=='/':
            lstr=''
            cmzt=''
            for i in range(len(message)):
                lstr+=message[i]
                if lstr=='/file':
                    i+=1
                    cmzt=message[i:]
                    cmzt = cmzt.split(' ')
                    if len(cmzt)==1:
                        print('Type "/file help" for get info.')
                    else:
                        if cmzt[1]=='help':
                            print('/file upload <path> - upload file to server.\n/file download - download file from server.\n/file list - view list of files on server.')
                        elif cmzt[1]=='upload':
                            if len(cmzt)>2:
                                while True:
                                    ask=str(input('[y/n]: '))
                                    if ask=='y':
                                        sendFile(cmzt[2])
                                        break
                                    elif ask=='n':
                                        print('Cancelled.')
                                        break
                                    else:
                                        print('Invalid answer.')
                                        continue
                            else:
                                print('Enter file path!')
                        elif cmzt[1]=='list':
                            send('104')
                        elif cmzt[1]=='download':
                            if len(cmzt)>2:
                                downloadFile(cmzt[2])
                                op72=1
                            else:
                                process('Enter file name!')
                    break
                elif lstr=='/list':
                    send('2421')
                    break
                elif lstr=='/exit':
                    send('-901')
                    return 0
        else:
            sendMsg(message)
while True:
    while True:
        hdef = str(input('address: '))

        HOST=''
        PORT=''
        r=0
        for i in range(len(hdef)):
            if hdef[i]==':':
                r=1
                continue
            if r==0:
                HOST+=hdef[i]
            if r==1:
                PORT+=hdef[i]
        PORT=int(PORT)
        try:
            s = socket.socket()
            s.connect((HOST, PORT))
            pswd=str(input('password: '))
            s.send(pswd.encode())
            dat = s.recv(1024)
            if dat.decode()=='True':
                print('Connected.')
                break
            else:
                print('Wrong password')
                continue
        except:
            print('Invalid data.')
            continue

    while True:
        login=str(input('login: '))
        s.send(login.encode())
        dat = s.recv(1024)
        if dat.decode()=='l':
            pswd2=str(input('password: '))
            s.send(pswd2.encode())
            dat = s.recv(1024)
            if dat.decode()=='111011':
                print('Successfully connected.')
                rcv = threading.Thread(target=recieve)
                rcv.start()
                gcv()
                s.close()
                close()
                break
            elif dat.decode()=='90012':
                print('Wrong password.')
                continue
        elif dat.decode()=='r':
            print('Account with this name not exists.\nYou can register new account with this name. If you dont want enter "-c"')
            new_pswd=str(input('password: '))
            if new_pswd=='-c':
                s.send(b'-c')
                continue
            s.send(new_pswd.encode())
            answ=s.recv(1024)
            if answ.decode()=='y':
                print('Account has successfully registered. Now you can login under this username.')
                continue
            elif answ.decode()=='i':
                print('Password - "-c" is not available')
                continue
            else:
                print('Something went wrong. Code - '+answ.decode())
                continue
        else:
            print('Server refuse your connection with code '+str(dat.decode()))
            continue