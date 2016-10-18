# -*- coding:utf8 -*-
""" SQLite read & insert """
# !/usr/bin/python
# Python:   3.5.1
# Platform: Windows
# Author:   Heyn (heyunhuan@gmail.com)
# Program:  SQLite.
# History:  2016/10/17

# (1) Limit all lines to a maximum of 79 characters
# (2) Private attrs use [__private_attrs]
# (3) [PyLint Message: See web: http://pylint-messages.wikidot.com/]

import os
import sys
import sqlite3
import logging


class CoraSQLite:
    """Cora SQLite Class."""

    def __init__(self, path=sys.path[0], debugLevel=logging.WARNING):
        super(CoraSQLite, self).__init__()
        self.path = path
        if os.path.exists(path) and os.path.isfile(path):
            self.conn = sqlite3.connect(path)
        else:
            self.conn = sqlite3.connect(':memory:')
        self.cursor = self.conn.cursor()

        formatopt = '[%(asctime)s] [%(filename)s] [%(levelname)s] %(message)s'
        logging.basicConfig(level=debugLevel, format=formatopt)
        # logging.basicConfig(
        # level=debugLevel, format=formatopt, filemode='w',
        # filename='logging.log')

    def __del__(self):
        self.close()

    def close(self):
        """Close SQLite Connect.
        Argument(s):
                    None
        Return(s):
                    None
        Notes:
                    2016-10-18 V1.0.0[Heyn]
        """

        if hasattr(self, "conn") and self.conn is not None:
            self.conn.close()

    def fetchall(self, querystr):
        """Fatch all data from sqlite.
        Argument(s):
                    querystr : SQL statement
        Return(s):
                    None
        Notes:
                    2016-10-18 V1.0.0[Heyn]
        """
        try:
            if querystr is not None and querystr != '':
                self.cursor = self.conn.cursor()
                self.cursor.execute(querystr)
                ret = self.cursor.fetchall()
                if len(ret) > 0:
                    for index, item in enumerate(ret):
                        print('Index = %d' % index, item)
            else:
                print('The [{}] is empty or equal None!'.format(querystr))
        except BaseException:
            print('Fetchall <ERROR>.')

    def execute_non_query(self, querystr):
        """Execute non query.
        Argument(s):
                    querystr : SQL statement
                    i.e.
                        CRATETABLE_SQL = '''CREATE TABLE `student` (
                                            `id` int(11) NOT NULL,
                                            `name` varchar(20) NOT NULL,
                                            `gender` varchar(4) DEFAULT NULL,
                                            `age` int(11) DEFAULT NULL,
                                            `address` varchar(200) DEFAULT NULL,
                                            `phone` varchar(20) DEFAULT NULL,
                                            PRIMARY KEY (`id`)
                                            )'''
                        CONN.execute_non_query(CRATETABLE_SQL)
        Return(s):
                    None
        Notes:
                    2016-10-18 V1.0.0[Heyn]
        """
        if querystr is not None and querystr != '':
            try:
                self.cursor = self.conn.cursor()
                self.cursor.execute(querystr)
                self.conn.commit()
            except BaseException:
                print('Execute_non_query <ERROR>.')
        else:
            print('The [{}] is empty or equal None!'.format(querystr))

    def execute(self, sql, data):
        """Execute SQL.
        Argument(s):
                    sql : SQL statement
                    data: Data for sql statement.
                    i.e.
                        sql = '''INSERT INTO tablename VALUES (?, ?, ?, ?, ?, ?)'''
                        data = [(1, 'Lily', 'M', 20, 'CN', '131******62'),
                                (2, 'Cate', 'F', 23, 'CN', '134******65')]
        Return(s):
                    None
        Notes:
                    2016-10-18 V1.0.0[Heyn]
        """

        if sql is not None and sql != '':
            if data is not None:
                try:
                    self.cursor = self.conn.cursor()
                    self.cursor.executemany(sql, data)
                    self.conn.commit()
                    # for item in data:
                    #     self.cursor.execute(sql, item)
                    #     self.conn.commit()
                except BaseException:
                    print('Execute [{}] <ERROR>.'.format(sql))
        else:
            print('The [{}] is empty or equal None!'.format(sql))

# if __name__ == '__main__':
#     CONN = CoraSQLite()

#     CRATETABLE_SQL = '''CREATE TABLE `student` (
#                            `id` int(11) NOT NULL,
#                            `name` varchar(20) NOT NULL,
#                            `gender` varchar(4) DEFAULT NULL,
#                            `age` int(11) DEFAULT NULL,
#                            `address` varchar(200) DEFAULT NULL,
#                            `phone` varchar(20) DEFAULT NULL,
#                             PRIMARY KEY (`id`)
#                          )'''
#     CONN.execute_non_query(CRATETABLE_SQL)

#     INSERT_SQL = '''INSERT INTO student values (?, ?, ?, ?, ?, ?)'''
#     DATA = [(1, 'Lee', 'F', 20, 'CN', '131******62'),
#             (2, 'Tom', 'F', 21, 'US', '132******63'),
#             (3, 'Jake', 'M', 22, 'JP', '133******64'),
#             (4, 'Cate', 'M', 23, 'CN', '134******65')]
#     CONN.execute(INSERT_SQL, DATA)
#     FETCH_ALL = '''SELECT * FROM student'''
#     CONN.fetchall(FETCH_ALL)
#     CONN.close()
