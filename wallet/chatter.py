# "Chatter" function from Project 1 that prints lines one character at a time
import time
import sys
from random import randrange

def chatter(npc_chatter):
    for c in npc_chatter:
        sys.stdout.write(c)
        sys.stdout.flush()
        secs = '0.01'# + str(randrange(10,20,1))
        secs = float(secs)
        time.sleep(secs)
    print()
    time.sleep(1)