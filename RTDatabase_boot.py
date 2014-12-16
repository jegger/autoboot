#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sqlite3 


class RTDatabase():
    """This class reads and writes the SQLite database"""
    def __init__(self):
        pass
        
    def open_database(self):
        self.DB_connection = sqlite3.connect("database.sqlite")
        self.DB_cursor = self.DB_connection.cursor()
    
    def close_database(self):
        self.DB_connection.close()
        
    def read_day(self, day):
        self.open_database()
        self.DB_cursor.execute("SELECT start_hour, start_min, stop_hour, stop_min FROM time WHERE day = '%s'" %day)
        self.DB_connection.commit()
        for row in self.DB_cursor:
            time = {"start_hour": row[0], "start_min": row[1],
                    "stop_hour": row[2], "stop_min": row[3]}
        self.close_database()
        return time
    
    def insert_day(self, day, start_hour, start_min, stop_hour, stop_min, stay_off):
        self.open_database()
        self.data = (start_hour, start_min, stop_hour, stop_min, stay_off, day)
        self.DB_sql = "UPDATE time SET start_hour = ?, start_min = ?, stop_hour = ?, stop_min = ?, stay_off = ? WHERE day = ?" 
        self.DB_cursor.execute(self.DB_sql, self.data)
        self.DB_connection.commit()
        self.close_database()


database = RTDatabase()
