# -*- coding:utf-8 -*-
import os
import logging
import cx_Oracle
from configs import (ORCL_HOST, ORCL_PASSWD, ORCL_PORT, ORCL_SERVICE_NAME,
                    ORCL_USER)

logger = logging.getLogger(__name__)


class OracleAccess(object):
    arraysize = None
    pool = None

    @staticmethod
    def initialise(min=1, max=2, increment=1, encoding="UTF-8"):
        os.environ['NLS_LANG'] = 'TRADITIONAL CHINESE_TAIWAN.AL32UTF8'
        OracleAccess.arraysize = 100
        try:
            OracleAccess.pool = cx_Oracle.SessionPool(
                ORCL_USER,
                ORCL_PASSWD,
                "%s:%s/%s" % (ORCL_HOST, ORCL_PORT, ORCL_SERVICE_NAME),
                min=min,
                max=max,
                increment=increment,
                encoding=encoding
            )
        except cx_Oracle.DatabaseError as e:
            error_obj, = e.args
            logger.error("%s: %s" % (error_obj.code, error_obj.message))
    
    @staticmethod
    def _get_conn():
        return OracleAccess.pool.acquire()
    
    @staticmethod
    def _get_cursor(conn, arraysize=None):
        cursor = conn.cursor()
        cursor.arraysize = arraysize if arraysize else OracleAccess.arraysize
        return cursor
    
    @staticmethod
    def query(sql, args=[], arraysize=None):
        """
        Args:
            sql(string)
        """
        try:
            conn = OracleAccess._get_conn()
            cursor = OracleAccess._get_cursor(conn=conn, arraysize=arraysize)
            cursor.execute(sql, args)
            data = cursor.fetchall()
            columns = [column[0].lower() for column in cursor.description]
            dict_data = [dict(zip(columns, row)) for row in data]
            return data, dict_data
        finally:
            if conn:
                OracleAccess.pool.release(conn)

    @staticmethod
    def query_by_offset(sql, arraysize=None, offset=0, numrows=20):
        """
        Args:
            sql(string)
        """
        try:
            conn = OracleAccess._get_conn()
            cursor = OracleAccess._get_cursor(conn=conn, arraysize=arraysize)
            cursor.execute(sql, offset=offset, numrows=numrows)
            return cursor.fetchall()
        finally:
            if conn:
                OracleAccess.pool.release(conn)

    @staticmethod      
    def insert(sql, rows, arraysize=None):
        """
        Args:
            sql(string)
            rows(list)
        """
        try:
            conn = OracleAccess._get_conn()
            cursor = OracleAccess._get_cursor(conn=conn, arraysize=arraysize)
            cursor.executemany(sql, rows)
            conn.commit()
        finally:
            if conn:
                OracleAccess.pool.release(conn)

    @staticmethod
    def execute(sql, args=[], arraysize=None):
        """
        Args:
            sql(string)
        """
        try:
            conn = OracleAccess._get_conn()
            cursor = OracleAccess._get_cursor(conn=conn, arraysize=arraysize)
            cursor.execute(sql, args)
            conn.commit()
        finally:
            if conn:
                OracleAccess.pool.release(conn)

    @staticmethod
    def data_exists(table_name, column_name='*', value: list = []):
        try:
            if column_name == '*':
                result = OracleAccess.query("SELECT * FROM %s" % table_name)
            else:
                sql = "SELECT * FROM %s WHERE %s = :1" % (table_name, column_name)
                result = OracleAccess.query(sql, value)
                if len(result) == 0:
                    raise cx_Oracle.DatabaseError
        except cx_Oracle.DatabaseError as e:
            return False
        else:
            return result

    @staticmethod
    def create_table(table_name, columns):
        """
        Args:
            table_name(string)
            columns(list)
        Example:
            columns = ['id number(10)', 'name varchar2(50)']
            columns = ['id number(10) PRIMARY KEY', 'name varchar2(50)', 'department_id number(10) REFERENCES departments(id)']
        """
        sql = "CREATE TABLE %s (%s)" % (table_name, ", ".join(columns))
        OracleAccess.execute(sql)
