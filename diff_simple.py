import sys
import secrets
import random


def generator(nrange):
    '''
    Returns a random integer from 0-nrange
    '''
    return random.randint(0,nrange)

def randomizer(realnum,nrange):
    '''
    Flips a coin in a cryptographically secure way. If that coin is heads,
    returns realnum. If tails, returns another randomly generated number,
    also cryptographically secure.
    '''
    flip = secrets.choice([0,1]) #flipping coin
    if flip: #heads
        return realnum
    elif flip == 0: #tails
        fakenum = secrets.randbelow(nrange+1) #randbelow is exclusive so +1
        return fakenum
    else raise RuntimeError("coin must be 0 or 1")

def db_creator():
    '''
    creates two lists, one with the real data and one with differentially
    private data
    '''
    db_real = []
    db_priv = []
