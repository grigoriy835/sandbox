import atexit

def exitd():
    with open('test.txt','w') as file:
        file.write('lol')
atexit.register(exitd)

from time import sleep

sleep(100)