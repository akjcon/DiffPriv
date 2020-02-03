import sys
from diff_classes import ColumnType,Database
from bitarray import bitarray
import hashlib
import random
import numpy as np
import matplotlib.pyplot as plt


def print_db(database):
    print('\n')
    for col in database:
        for obj in col:
            print(obj,end=' ')
        print('|')
    print('\n')

def query_db(database,column,hash_num):
    # column is column index
    datacol = database[column] #should be ColumnType object
    type = datacol.type
    ret_col = []
    if type == 'bool':
        # do the simple randomized response thing
        for data in datacol:
            c = random.randint(0,1)
            if c == 0:
                ret_col.append(data)
            else: ret_col.append(bool(random.randint(0,1)))
        return ColumnType(type,ret_col)
    elif type == 'int' or type == 'string':
        # do the bloom filter
        for data in datacol:
            ret_col.append(to_bloom_filter(data,hash_num))
        return ColumnType(type,ret_col)
    else: return 'data not in correct format'

def get_bloom_bits(datum,hash_num):
    #returns bloom filter w correct bits set
    md5 = hashlib.md5(str(datum).encode('utf-8'))
    hash = md5.digest()
    bloom_bits = [hash[i] for i in range(hash_num)] #gets bits to flip in bitarray

    b = bitarray(2**8) #initializing blank 256 bit bloom filter
    b.setall(0) #zeroing
    for num in bloom_bits:
        b[num] = True
    return b

def to_bloom_filter(datum,hash_num):
    '''
    takes one data point (eg 'banana') and hashes it to a bloom filter B.
    then, we take this bloom filter (a bit array), and iterate through it
    and let each bit have .25 chance of being a 1 or a 0, and a .5 chance
    of being the original value from B. We then report this new bloom filter
    B' and insert it into a new database
    datum: value to be hashed
    hash_num: number of hashes to perform, must be 16 or less due to md5
    '''
    b = get_bloom_bits(datum,hash_num)

    b_mask = bin(random.randint(0, 2**256 - 1)) #random bloom filter
    b_mask_str = str(b_mask[2:]).zfill(256) #padding with zeroes
    b_mask = bitarray([int(i) for i in b_mask_str]) #converting to bitarray obj

    for index,bit in enumerate(b):
        c = random.randint(0,1)
        if c == 0:
            b[index] = b_mask[index]
        else: pass

    #bitarray is randomized, differentially private now
    return b

def testing():

    booldata = ColumnType('bool',[True,False,True,True,True,True,False,False,True,False])
    intdata = ColumnType('int',[int(round(np.random.normal(50,4))) for _ in range(10000)])
    stringdata = ColumnType('string',['peach','pear','apple','orange','grape',
                                          'banana','kiwi','mango','guava','nectarine'])
    testdata = [booldata,intdata,stringdata]

    std_db = Database('std',testdata) #new normal database
    diff_db = Database('diff',[]) # new empty differential database

    diff_db.add_row(query_db(std_db,0,4)) #adding rows to diff db
    diff_db.add_row(query_db(std_db,1,4))
    diff_db.add_row(query_db(std_db,2,4))
    #print_db(std_db)
    #print_db(diff_db)
    #testing whether the nums are in the bloom filters
    res = [] #array of numbers in bloom filter
    eq = True
    for i in range(100):
        bbits = get_bloom_bits(i,4)
        search = bbits.search(bitarray('1'))
        for row in diff_db[1]:
            eq = True
            for index in search:
                #print('Number: {}'.format(i))
                #print('Bloom bits: {}'.format(bbits))
                #print('Bloom bit indices: {}'.format(search))
                #print('Row to search: {}'.format(row))
                if row[index] != 1:
                    eq = False
                #print(eq)
                #print('\n')
            if eq == True: res.append(i)



    plt.subplot(2, 1, 1)
    plt.hist(std_db[1].column,bins='auto')
    plt.title('Normal data')
    plt.subplot(2, 1, 2)
    plt.hist(res,bins='auto',range=(35,65))
    plt.title('Differential data')
    plt.show()

if __name__ == '__main__':
    testing()
