import os
import time

os.system('pip install -r requirements-linux.txt')

def cleanscreen():
    if os.name == 'nt':
        os.system('clr')
    else:    os.system('clear')

while True:
    os.system('python ./GetNodes.py 3')
    os.system('git add .')
    os.system('git commit -m "update"')
    os.system('git push')
    # cleanscreen()

    time.sleep(7200)
