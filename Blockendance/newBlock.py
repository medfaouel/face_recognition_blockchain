from block import *
import datetime as dt
from attendance import ListToBlockchain
list=ListToBlockchain()

def next_block(last_block, data):
    this_index = last_block.index + 1
    this_timestamp = dt.datetime.now()
    # A one level deep copy of data has been created since data is modified repeatedly
    # in the calling function and if data is a direct pointer, it leads to modification
    # of old data in the chain.
    this_data = data[:]
    this_prev_hash = last_block.hash
    return Block(this_index, this_timestamp, this_data, this_prev_hash)

def add_block(form, data, blockchain):
    data.append([])
    i = 1
    if(form is not None):
        while form.get("roll_no{}".format(i)):
            
            data[-1].append(form.get("roll_no{}".format(i)))
            i += 1
        
    print("data1: ",data)
    previous_block = blockchain[-1]
    block_to_add = next_block(previous_block, data)
    blockchain.append(block_to_add)
    previous_block = block_to_add
    bc_string = str(data[0]) + " " + str(data[1]) + " " + str(data[2])
    for i in range(len(data[4])):
        if (i != len(data[4]) - 1):
            bc_string += " " + str(i + 1) + ":" + str(data[4][i]) + ","
        else:
            bc_string += " " + str(i + 1) + ":" + str(data[4][i])
    print(bc_string)
    return bc_string
    
def auto_add_block(form, data, blockchain):
    data.append([])
    i = 1
    if(form is not None):
        while form.get("roll_no{}".format(i)):
            i += 1
    for j in range(1,i):
        if(str(j) in list):
            data[-1].append('P')
        else:
            data[-1].append('A')
    print("Auto data : ",data)
    previous_block = blockchain[-1]
    block_to_add = next_block(previous_block, data)
    blockchain.append(block_to_add)
    previous_block = block_to_add
    bc_string = str(data[0]) +" " + str(data [1]) +" " +str(data [2])
    for i in range(len(data[4])):
        if(i!=len(data[4])-1):
            bc_string += " " + str(i+1) + ":" + str(data[4][i]) + ","
        else:
            bc_string += " " + str(i+1) + ":" + str(data[4][i])
    print(bc_string)
    return bc_string

