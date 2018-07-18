"""Implement two flask commands for loading and altering by CLI.

Command:
flask mongo load
    load fruits.csv into mongodb using func_read_data_for_insertion

flask mongo alter
    alter fruits.csv and mongodb using func_read_data_for_update
"""

import datetime
import csv
import traceback
import time
import os

import click
from flask import Flask
from flask.cli import AppGroup
from pymongo import MongoClient
from pymongo import bulk
import pandas as pd
import numpy as np


def is_int_float(input):
    """Check the numeric type of input.

    Arguments:
    input -- the examinied string

    Return:
    If input is an integer, return 'int'.
    If input is a float, return 'float'.
    Neither case, return 'none'.
    """

    try:
        int(input)
        return 'int'
    except ValueError:
        pass

    try:
        float(input)
        return 'float'
    except ValueError:
        return 'none'

def func_read_data_for_insertion(np_df):
    """Process np_df then feed it into func_insert_doc.

    Arguments:
    np_df -- numpy.array of the csv file

    Return:
    the number of inserted documents
    """

    insert_doc_many = []
    for one_row in np_df:
        insert_doc = dict(zip(['sid', 'fruit', 'amount', 'price'], one_row))
        insert_doc['datetime'] = str(datetime.datetime.now())

        insert_doc_many.append(insert_doc)

    func_insert_doc(insert_doc_many, True)

    for one_doc in insert_doc_many:
    	print('Load \n', one_doc, '\n')

    return len(insert_doc_many)

def func_insert_doc(insert_doc, is_insert_many):
    """Insert data into mongodb. Use pymongo.bulk to batchly-insert documents. 
    Duplicates will be discarded.

    Arguments:
    insert_doc -- documents to be inserted
    """

    uri = 'mongodb://deckenkang66:97155434@db:27017/Pluvio'
    # uri = 'mongodb://db:27017/Pluvio'
    db = 'Pluvio'
    collection = 'fruits'

    client, collect = connect_to_db(uri, db, collection)

    while True:
        try:
            bulk_ = bulk.BulkOperationBuilder(collect, ordered=True)
            for doc in insert_doc:
                bulk_.find({"sid": doc["sid"], "fruit": doc['fruit'] }).upsert().update({
                    "$setOnInsert": doc
                })
            response = bulk_.execute()

            break
        except:
            print(traceback.format_exc())
            time.sleep(1)

    client.close()

def func_read_data_for_update(np_df, write_to_csv=True):
    """Read np_df, capitalize strings and increment int/float by 1.

    Arguments:
    np_df -- numpy.array of the csv file
    write_to_csv -- True means writing modified data into a new csv file

    Return:
    the number of updated documents
    """


    if write_to_csv:
        restored_csv = []

    for one_row in np_df:
        one_row_backup = []  # store the old row to find rows for updating

        for index in range(len(one_row)):
            type_check = is_int_float(one_row[index])
            if type_check.startswith('float'):
                one_row_backup.append(float(one_row[index]))
                one_row[index] = float(one_row[index]) + 1.0
            elif type_check.startswith('int'):
                one_row_backup.append(int(one_row[index]))
                one_row[index] = int(one_row[index]) + 1
            else:
                one_row_backup.append(one_row[index])
                one_row[index] = one_row[index].upper()

        func_update_doc(
        	{'sid':one_row_backup[0], 'fruit':one_row_backup[1]},
        	{   
                'sid':one_row[0], 'fruit':one_row[1], 
                'amount':one_row[2], 'price':one_row[3]
            }
        )

        print(one_row_backup, 'to', one_row)
        
        if write_to_csv:
            restored_csv.append(one_row)

    if write_to_csv:
        func_write_to_csv(restored_csv)

    return len(restored_csv)

def func_update_doc(condition_dict, update_dict):
    """Update existing data of mongodb

    Arguments:
    condition_dict -- documents to be updated
    update_dict -- updating data
    """

    uri = 'mongodb://deckenkang66:97155434@db:27017/Pluvio'
    # uri = 'mongodb://db:27017/Pluvio'
    db = 'Pluvio'
    collection = 'fruits'

    client, collect = connect_to_db(uri, db, collection)

    while True:
        try:
            collect.update_one({
                    'sid': condition_dict['sid'], 'fruit': condition_dict['fruit']
                }, {
                    '$set': {
                        'sid': update_dict['sid'],
                        'fruit': update_dict['fruit'],
                        'amount': update_dict['amount'],
                        'price': update_dict['price'],
                    }
                }, upsert=False
            )

            break
        except:
            print(traceback.format_exc())
            time.sleep(1)

    client.close()

def func_write_to_csv(restored_csv):
    """write data into fruits.csv and rename the old csv with timestamp

    Arguments:
    restored_csv -- data of fruits.csv
    """

    os.rename('fruits.csv', 'fruits_{}.csv'.format(str(int(time.time()))))

    with open('fruits.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)

        for one_row in restored_csv:
          writer.writerow(one_row)

def connect_to_db(uri, db, collection):
    """Set up mongodb connection

    Arguments:
    uri -- mongodb uri
    db -- which database
    collection -- which collection

    returns:
    MongoClient, MongoClient with assigned database and collection
    """

    client = MongoClient(uri)

    client_db = client[db]
    client_collect = client_db[collection]

    return client, client_collect

app = Flask(__name__)
mongo_cli = AppGroup('mongo')

@mongo_cli.command('load')
def mongo_insertion():
    """Insert documents from a csv file"""

    # header=None: no header row available,
    # treat the first row as data
    df = pd.read_csv('fruits.csv', header=None)  
    np_df = np.array(df)

    print('Start loading...')
    number_insertion = func_read_data_for_insertion(np_df)
    print('Load {} documents...'.format(number_insertion))
    print('Duplicate documents will be discarded...\n')

    print('Enter \'py.test test_class.py -k test_load\' to examine the program reliability.')


@mongo_cli.command('alter')
def mongo_update():
    """Update documents based on a csv file"""

    df = pd.read_csv('fruits.csv', header=None)
    np_df = np.array(df)

    print('Start altering...')
    number_update = func_read_data_for_update(np_df)
    print('Alter {} documents...\n'.format(number_update))

    print('Enter \'py.test test_class.py -k test_alter\' to examine the program reliability.')


app.cli.add_command(mongo_cli)