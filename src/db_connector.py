# -*- coding: utf-8 -*-
import psycopg2

class DatabaseConnector(object):
    def __init__(self, account):
        self.account = account
    
    def __enter__(self): 
        self.connect = psycopg2.connect(
            host=self.account['host'],
            dbname=self.account['db'],
            user=self.account['user'],
            password=self.account['password']
        )
        return self.connect
    
    def __exit__(self, exception_type, exception_value, traceback):
        self.connect.close()
