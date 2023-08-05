import datetime
import logging
import re
from enum import Enum

from db_hammer.entity_util import update_sql, insert_sql, delete_sql

from db_hammer.csv import start as csv_start
from db_hammer.sql_exception import SqlException
from db_hammer.util.date import date_to_str


class DataType(Enum):
    DateNull = -2177774
    DataPass = -2177771


class BaseConnection(object):
    def __init__(self, **kwargs):
        """
        :param kwargs:
        """
        self.log = kwargs.get("log", logging.getLogger(__name__))
        self.Db_NAME = kwargs.get("db_name")
        self.conn = None  # type:Connect
        self.cursor = None  # type:cursor
        self.table_column_cache = {}

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def select_page_size(self, sql: str, params: dict = None, page_size=50) -> int:
        """
        根据sql获取页数
        :param params:
        :param sql:
        :param page_size: 分页大小
        :return: 页数
        """

        count_sql = "select COUNT(0) from ( %s ) temp_count" % sql
        count_sql = self.sql_params(count_sql, params)
        self.log.debug("execute sql :" + count_sql.replace("\n", " "))
        self.cursor.execute(count_sql, params)
        data = self.cursor.fetchone()
        self.log.debug("fetch rows:" + str(len(data)))
        num = data[0] // page_size
        if data[0] > page_size * num:
            num = num + 1
        return num

    def sql_params(self, sql: str, params: dict):
        if params is None:
            return sql
        ps = re.findall('(?<!\w):\w+', sql)
        start = 0
        for p in ps:
            if p[1:] not in params or len(p) == 1:
                raise SqlException(f"SQL语句中参数[{p}]没有传值")
            start = sql.find(p, start)
            param = "%(" + p[1:] + ")s"
            sql = sql[:start] + param + sql[start + len(p):]
            start += len(param)
        return sql

    def select_page_list(self, sql: str, page_size=50, page_start=1, **kwargs) -> list:
        """
        获取分页列表数据,列表方式返回
        :param sql:
        :param page_size: 分页大小
        :param page_start: 开始页 （从1开始）

        **kwargs
        page_end: 结束页 defalut：page_start+1
        add_headers: 是否添加表头 defalut:False
        :return:
        """
        params = kwargs.get("params", None)
        page_end = kwargs["page_end"]
        if page_end is None:
            page_end = page_start + 1
        add_headers = kwargs["add_headers"]
        if add_headers is None:
            add_headers = False

        start = page_size * (page_start - 1)
        end = page_size * (page_end - 1)
        page_sql = """select * FROM (select temp_page.*, rownum row_id from 
                         ( %s ) temp_page 
                       where limit %d,%d
                       """ % (sql, end, start)
        page_sql = self.sql_params(page_sql, params)
        self.log.debug("execute sql :" + page_sql.replace("\n", " "))
        self.cursor.execute(page_sql, params)
        data = self.cursor.fetchall()
        self.log.debug("fetch rows:" + str(len(data)))
        if add_headers:
            col_names = self.cursor.description
            list(data).insert(col_names, 0)
        return data

    def select_dict_page_list(self, sql: str, page_size=50, page_start=1, **kwargs) -> list:
        """
        获取分页列表数据，,字典形式返回
        :param sql:
        :param page_size:
        :param page_start:
        :param page_end:
        :return:
        """

        page_end = kwargs.get("page_end", page_start + 1)
        add_headers = kwargs.get("add_headers", False)
        params = kwargs.get("params", None)
        data = self.select_page_list(sql, page_size, page_start, params=params,
                                     page_end=page_end,
                                     add_headers=add_headers)
        col_names = self.cursor.description
        return self._data_to_map(col_names, data)

    def select_value(self, sql: str, params=None) -> str:
        """
        获取第一列第一行的值
        :param sql:
        :return:
        """
        self.log.debug("execute sql :" + sql.replace("\n", " "))
        _sql = self.sql_params(sql, params)
        self.cursor.execute(_sql, params)
        data = self.cursor.fetchone()
        if data is None:
            return None
        return str(data[0])

    def select_list(self, sql: str, params=None) -> list:
        """
        获取列表数据,列表方式返回
        :param sql:
        :return:
        """
        self.log.debug("execute sql :" + sql.replace("\n", " "))
        _sql = self.sql_params(sql, params)
        self.cursor.execute(_sql, params)
        data = self.cursor.fetchall()
        self.log.debug("fetch rows:" + str(len(data)))
        return data

    def select_dict_list(self, sql: str, params=None) -> list:
        """
        获取查询语句列表数据，以字典方式返回: List<dict>
        :param params:
        :param sql:
        :return:
        """
        self.log.debug("execute sql :" + sql.replace("\n", " "))
        _sql = self.sql_params(sql, params)
        self.cursor.execute(_sql, params)
        data = self.cursor.fetchall()
        self.log.debug("fetch rows:" + str(len(data)))
        col_names = self.cursor.description
        return self._data_to_map(col_names, data)

    def select_dict(self, sql: str, params=None) -> dict:
        """
        获取字典数据，以字典方式返回: dict
        :param params:
        :param sql:
        :return:
        """
        data = self.select_dict_list(sql, params)
        if data is None or len(data) == 0:
            return None
        return data[0]

    @staticmethod
    def _data_to_map(col_names, data):
        r_list = []
        for k in range(len(data)):
            row = {}
            for i in range(len(col_names)):
                row[col_names[i][0]] = data[k][i]
            r_list.append(row)
        return r_list

    def execute(self, sql: str, params=None) -> int:
        """
        执行sql,并返回影响行数
        :param params:
        :param sql:
        :return:
        """
        # self.log.debug("execute sql :" + sql.replace("\n", " "))
        self.cursor.execute(sql, params)
        i = self.cursor.rowcount
        self.log.debug("fetch rows:" + str(i))
        return i

    def close(self):
        self.conn.close()
        self.log.debug("conn close")

    def rollback(self):
        """回滚事务"""
        self.log.debug("rollback start")
        self.conn.rollback()
        self.log.debug("rollback end")

    def commit(self):
        """提交事务，如果有对数据库进更新，需要手动提交事务
        """
        self.log.debug("commit start")
        self.conn.commit()
        self.log.debug("commit end")
        return

    def db_data_type_mapping(self):
        """数据库与Python类型映射
            key: 数据库类型
            value: Py类型
            默认为MySQL数据库
        """

        return {
            "CHAR,VARCHAR,TINYBLOB,TINYTEXT,BLOB,TEXT,MEDIUMBLOB,MEDIUMTEXT,LONGBLOB,LONGTEXT": str,
            "TINYINT,SMALLINT,MEDIUMINT,INT,INTEGER,BIGINT": float,
            "FLOAT,DOUBLE,DECIMAL": int,
            "DATE,TIME,YEAR,DATETIME,TIMESTAMP": "STR_TO_DATE('${VALUE}', '%Y-%m-%d %H:%i:%s')",
        }

    def __get_py_type(self, db_type):
        dtm = self.db_data_type_mapping()
        for dt in dtm.keys():
            dd = dt.split(",")
            if str(db_type).upper() in dd:
                return dtm[dt]
        raise Exception("不支持的数据库类：" + str(db_type))

    def db_column_sql(self, table_name):
        """
        获取数据列的SQL
        占位参数：
            ${TABLE_NAME} : 表名
            ${DB_NAME} : 连接的数据库名

        :return:
            COLUMN_NAME : 名称
            DATA_TYPE ： 类型
            COMMENTS ： 备注
            DATA_LENGTH ： 长度
            DATA_PRECISION ：精度
        """
        return f"""
            SELECT 
             COLUMN_NAME AS COLUMN_NAME,
            DATA_TYPE AS DATA_TYPE,
            COLUMN_COMMENT AS COMMENTS,
            CHARACTER_MAXIMUM_LENGTH AS DATA_LENGTH,
            NUMERIC_PRECISION AS DATA_PRECISION
             FROM INFORMATION_SCHEMA.COLUMNS T
             WHERE 
             TABLE_NAME = '{table_name}' AND TABLE_SCHEMA = '{self.Db_NAME}'
            """

    def gen_insert_dict_sql(self, dict_data: dict, table_name: str):
        """
        通过字典保存数据，字典的key为表列表
        :param dict_data:
        :param table_name:
        :return:
        """
        columns = self.__select_db_columns(table_name=table_name)
        values = {}
        if dict_data is not None:
            for c in columns:
                column_name = c.get("COLUMN_NAME", None) if c.get("COLUMN_NAME", None) is not None else c["column_name"]
                data_type = c.get("DATA_TYPE", None) if c.get("DATA_TYPE", None) is not None else c["data_type"]
                values[column_name] = self.__get_column_value(data_type=data_type, value=dict_data[column_name])
        else:
            return None
        sql = f"""INSERT INTO {self.Db_NAME}.{table_name} ({','.join(values.keys())}) VALUES ({','.join(values.values())})"""
        return sql

    def __get_column(self, name, columns):
        for c in columns:
            column_name = c.get("COLUMN_NAME", None) if c.get("COLUMN_NAME", None) is not None else c["column_name"]
            if column_name == name:
                return c
        return None

    def __select_db_columns(self, table_name):
        cache = self.table_column_cache.get(table_name, None)
        if cache is not None:
            return cache
        else:
            columns = self.select_dict_list(sql=self.db_column_sql(table_name=table_name))
            self.table_column_cache[table_name] = columns
            return columns

    def gen_update_dict_sql(self, dict_data: dict, table_name: str, where: str, not_update_colunms=[]):
        """
        根据字典生成Update语句
        :param dict_data:  列新字典
        :param table_name: 表名
        :param where: 带上where条件
        :return:
        """
        columns = self.__select_db_columns(table_name=table_name)
        values = {}
        if dict_data is not None:
            for column_name in dict_data.keys():
                column = self.__get_column(column_name, columns)
                if column is not None:
                    data_type = column.get("DATA_TYPE", None) if column.get("DATA_TYPE", None) is not None else column[
                        "data_type"]
                    values[column_name] = self.__get_column_value(data_type=data_type, value=dict_data[column_name])
        else:
            return None
        sets = []
        for c in values.keys():
            if c not in not_update_colunms:
                sets.append(f"{c}={values[c]}")
        update_sql = f"UPDATE {self.Db_NAME}.{table_name} SET {','.join(sets)} " + where
        return update_sql

    def __get_column_value(self, data_type, value):
        """获取列的值"""
        if data_type is None:
            return f"'{self.convert_str(value)}'"
        t = self.__get_py_type(db_type=data_type)
        if value is None:
            return "null"
        elif t == str:
            return f"'{self.convert_str(value)}'"
        elif t in (int, float):
            return str(value)
        else:
            if isinstance(value, (datetime.datetime, datetime.date)):
                return t.replace("${VALUE}", date_to_str(value))
            else:
                return t.replace("${VALUE}", self.convert_str(value))

    def select_insert_sql(self, sql: str, table_name: str) -> list:
        """根据SQL查询数据并生成Insert语句"""
        records = self.select_dict_list(sql=sql)
        sql_list = []
        for r in records:
            sql = self.gen_insert_dict_sql(dict_data=r, table_name=table_name)
            sql_list.append(sql)
        return sql_list

    def convert_str(self, s: str):
        return str(s)

    def export_data_file(self, sql, dir_path, file_mode="txt", pack_size=500000, bachSize=10000, add_header=True,
                         data_split_chars=',',
                         data_close_chars='"', encoding="utf-8", outingCallback=None):
        """导出数据文件
        @:param sql 导出时的查询SQL
        @:param dir_path 导出的数据文件存放目录
        @:param file_mode 导出文件格式：txt|gz|csv
        @:param add_header 数据文件是否增加表头
        @:param pack_size  每个数据文件大小，默认为50万行，强烈建议分割数据文件，单文件写入速度会越来越慢
        @:param bachSize   游标大小
        @:param data_split_chars 每条数据字段分隔字符,csv文件默认为英文逗号
        @:param data_close_chars 每条数据字段关闭字符,csv文件默认为英文双引号
        @:param encoding 文件编码格式，默认为utf-8
        @:param outingCallback 导出过程中的回调方法
        """
        csv_start(cursor=self.cursor,
                  sql=sql,
                  path=dir_path,
                  bachSize=bachSize,
                  PACK_SIZE=pack_size,
                  file_mode=file_mode,
                  add_header=add_header,
                  CSV_SPLIT=data_split_chars,
                  CSV_FIELD_CLOSE=data_close_chars,
                  encoding=encoding,
                  callback=outingCallback,
                  log=self.log)

    def insert_entity(self, entity):
        """传入实体保存到数据库"""
        sql, values = insert_sql(entity=entity)
        self.log.debug(sql)
        self.log.debug(f"params:{values}")
        sql = self.sql_params(sql, values)
        i = self.execute(sql, values)
        self.commit()
        return i

    def update_entity(self, entity, pass_null=False):
        sql, values = update_sql(entity=entity, pass_null=pass_null)
        self.log.debug(f"SQL:{sql}")
        self.log.debug(f"params:{values}")
        sql = self.sql_params(sql, values)
        i = self.execute(sql, values)
        self.commit()
        return i

    def delete_entity(self, entity):
        sql, values = delete_sql(entity=entity)
        self.log.debug(sql)
        self.log.debug(f"params:{values}")
        sql = self.sql_params(sql, values)
        i = self.execute(sql, values)
        self.commit()
        return i

    def select_entity_list(self):
        print("select_list_by_columns")

    def select_entity_one(self):
        print("select_one_by_columns")
