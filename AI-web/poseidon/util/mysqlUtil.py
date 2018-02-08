# -*- coding: utf-8 -*-
import MySQLdb

class MySQLUtil():

    @staticmethod
    def createCursor(host,user,passwd,db):
        db = MySQLdb.connect(host= host,user=user,passwd=passwd,db = db)
        return db

    @staticmethod
    def exe_select_sql(db,sql):
        cursor = db.cursor()
        cursor.execute(sql)
        tup = cursor.fetchall()
        db.close()
        return tup

    @staticmethod
    def exe_update_sql(db,sql):
        cursor = db.cursor()
        try:
            result =cursor.execute(sql)
            db.commit()
            return result
        except Exception as e:
            db.rollback()

