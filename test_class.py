from pymongo import MongoClient
import pandas as pd
import numpy as np

class TestClass:
    def is_int_float(self, input):
        '''Check the numeric type of the input.

        If the input is an integer, return 'int'.
        If the input is a float, return 'float'.
        Neither case, return 'none' '''

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

    def connect_to_db(self, uri, db, collection):
        client = MongoClient(uri)

        client_db = client[db]
        client_collect = client_db[collection]

        return client, client_collect

    def test_load(self):
        uri = "mongodb://deckenkang66:97155434@db:27017/Pluvio"
        # uri = "mongodb://db:27017/Pluvio"
        db = 'Pluvio'
        collection = 'fruits'

        client, collect = self.connect_to_db(uri, db, collection)

        df = pd.read_csv('fruits.csv', header=None)
        np_df = np.array(df)

        for one_row in np_df:
            for index in range(len(one_row)):
                type_check = self.is_int_float(one_row[index])

                if type_check=='float':
                    one_row[index] = float(one_row[index])
                elif type_check=='int':
                    one_row[index] = int(one_row[index])

            find_result = collect.find_one({'sid':one_row[0], 
                                            'fruit':one_row[1], 
                                            'amount':one_row[2], 
                                            'price':one_row[3]})

            assert find_result is not None

        client.close()

    def test_alter(self):
        uri = "mongodb://deckenkang66:97155434@db:27017/Pluvio"
        # uri = "mongodb://db:27017/Pluvio"
        db = 'Pluvio'
        collection = 'fruits'

        client, collect = self.connect_to_db(uri, db, collection)

        df = pd.read_csv('fruits.csv', header=None)
        np_df = np.array(df)

        for one_row in np_df:
            for index in range(len(one_row)):
                type_check = self.is_int_float(one_row[index])

                if type_check=='float':
                    one_row[index] = float(one_row[index])
                elif type_check=='int':
                    one_row[index] = int(one_row[index])

            find_result = collect.find_one({'sid':one_row[0], 
                                            'fruit':one_row[1], 
                                            'amount':one_row[2], 
                                            'price':one_row[3]})

            assert find_result is not None

        client.close()
